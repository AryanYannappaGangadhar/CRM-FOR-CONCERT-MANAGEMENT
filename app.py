import os
import sqlite3
import random
import string
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort

app = Flask(__name__)
app.secret_key = 'event-ticket-booking-secret-key-2026'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'ticket_booking.db')

# ============================================================
# DATABASE HELPERS
# ============================================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    conn = get_db()
    conn.executescript(sql_script)
    conn.close()
    generate_seats_for_all_events()

def generate_seats_for_event(event_id, venue_capacity):
    rows_needed = (venue_capacity // 15) + 1
    rows = [chr(65 + i) for i in range(min(rows_needed, 26))]
    classes = ['VIP', 'Premium', 'Standard', 'Economy']
    seat_batch = []
    for row_idx, row in enumerate(rows):
        seat_class = classes[min(row_idx // max(1, (len(rows) // 4 + 1)), 3)]
        seats_in_row = min(15, venue_capacity - (row_idx * 15))
        for num in range(1, seats_in_row + 1):
            seat_batch.append((row, str(num), seat_class, 'Available', event_id))
    conn = get_db()
    try:
        conn.executemany(
            'INSERT OR IGNORE INTO SEAT (seat_row, seat_number, seat_class, seat_status, event_id) VALUES (?,?,?,?,?)',
            seat_batch
        )
        conn.commit()
    finally:
        conn.close()

def generate_seats_for_all_events():
    events = query_db('SELECT e.event_id, v.total_capacity FROM EVENT e JOIN VENUE v ON e.venue_id = v.venue_id')
    for e in events:
        existing = query_db('SELECT COUNT(*) as cnt FROM SEAT WHERE event_id=?', (e['event_id'],), one=True)
        if existing['cnt'] == 0:
            generate_seats_for_event(e['event_id'], e['total_capacity'])

# ============================================================
# AUTH DECORATORS
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('user_role') != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def generate_ref(prefix):
    ts = datetime.now().strftime('%Y%m%d')
    rand = ''.join(random.choices(string.digits, k=6))
    return f'{prefix}{ts}{rand}'

def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

DEMO_CREDENTIALS = {
    'admin@ticketbook.com': 'admin123',
    'rajesh@email.com': 'rajesh123',
    'priya@email.com': 'priya123',
    'amit@email.com': 'amit123',
}

def check_password(stored_hash, input_password, user_email=None):
    from werkzeug.security import check_password_hash
    try:
        return check_password_hash(stored_hash, input_password)
    except Exception:
        if user_email and user_email in DEMO_CREDENTIALS:
            return input_password == DEMO_CREDENTIALS[user_email]
        return stored_hash == input_password

def calculate_refund(event_date_str, total_amount):
    event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
    days_diff = (event_date - datetime.now().date()).days
    if days_diff > 7:
        return total_amount, '100% refund (More than 7 days before event)'
    elif days_diff >= 3:
        return total_amount * 0.5, '50% refund (3-7 days before event)'
    else:
        return 0, '0% refund (Less than 3 days before event - No refund policy)'

def current_user():
    if 'user_id' in session:
        return query_db('SELECT * FROM CUSTOMER WHERE customer_id=?', (session['user_id'],), one=True)
    return None

# ============================================================
# ROUTES: HOME & AUTH
# ============================================================
@app.route('/')
def home():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    query = 'SELECT e.*, v.venue_name, v.address FROM EVENT e JOIN VENUE v ON e.venue_id = v.venue_id WHERE e.event_status = ?'
    args = ['Published']
    if category:
        query += ' AND e.category = ?'
        args.append(category)
    if search:
        query += ' AND (e.event_name LIKE ? OR e.description LIKE ?)'
        args.extend([f'%{search}%', f'%{search}%'])
    query += ' ORDER BY e.event_date ASC'
    events = query_db(query, args)
    categories = ['Concert', 'Conference', 'Sports', 'Theater', 'Workshop', 'Other']
    return render_template('home.html', events=events, categories=categories, selected_cat=category, search=search, user=current_user())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['full_name'].strip()
        email = request.form['email'].strip().lower()
        phone = request.form['phone'].strip()
        password = request.form['password']
        address = request.form.get('address', '')
        existing = query_db('SELECT customer_id FROM CUSTOMER WHERE email=?', (email,), one=True)
        if existing:
            flash('Email already registered.', 'danger')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
        else:
            try:
                cid = execute_db(
                    'INSERT INTO CUSTOMER (full_name, email, phone, password_hash, address, user_role) VALUES (?,?,?,?,?,?)',
                    (name, email, phone, hash_password(password), address, 'Customer')
                )
                session['user_id'] = cid
                session['user_role'] = 'Customer'
                session['user_name'] = name
                flash('Registration successful! Welcome aboard.', 'success')
                return redirect(url_for('home'))
            except Exception as ex:
                flash(f'Error: {ex}', 'danger')
    return render_template('register.html', user=current_user())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = query_db('SELECT * FROM CUSTOMER WHERE email=?', (email,), one=True)
        if user and check_password(user['password_hash'], password, user_email=email):
            session['user_id'] = user['customer_id']
            session['user_role'] = user['user_role']
            session['user_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or (url_for('admin_dashboard') if user['user_role'] == 'Admin' else url_for('home')))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', user=current_user())

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    bookings = query_db(
        'SELECT b.*, e.event_name, e.event_date, e.event_time, v.venue_name FROM BOOKING b '
        'JOIN EVENT e ON b.event_id = e.event_id JOIN VENUE v ON e.venue_id = v.venue_id '
        'WHERE b.customer_id=? ORDER BY b.booking_date DESC',
        (session['user_id'],)
    )
    return render_template('profile.html', user=current_user(), bookings=bookings)

# ============================================================
# MODULE 1: EVENT & VENUE MANAGEMENT
# ============================================================
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = query_db(
        'SELECT e.*, v.venue_name, v.address, v.total_capacity, v.amenities FROM EVENT e '
        'JOIN VENUE v ON e.venue_id = v.venue_id WHERE e.event_id=?', (event_id,), one=True
    )
    if not event:
        abort(404)
    ticket_types = query_db('SELECT * FROM TICKET_TYPE WHERE event_id=? ORDER BY price DESC', (event_id,))
    return render_template('event_detail.html', event=event, ticket_types=ticket_types, user=current_user())

@app.route('/admin/events')
@admin_required
def admin_events():
    events = query_db(
        'SELECT e.*, v.venue_name, (SELECT COUNT(*) FROM BOOKING b WHERE b.event_id=e.event_id AND b.booking_status="Confirmed") as bookings_count '
        'FROM EVENT e JOIN VENUE v ON e.venue_id = v.venue_id ORDER BY e.event_date DESC'
    )
    return render_template('admin/events.html', events=events, user=current_user())

@app.route('/admin/events/create', methods=['GET', 'POST'])
@admin_required
def create_event():
    venues = query_db('SELECT * FROM VENUE ORDER BY venue_name')
    if request.method == 'POST':
        eid = execute_db(
            'INSERT INTO EVENT (event_name, event_date, event_time, description, category, event_status, banner_image, venue_id) VALUES (?,?,?,?,?,?,?,?)',
            (request.form['event_name'], request.form['event_date'], request.form['event_time'],
             request.form['description'], request.form['category'], request.form['event_status'],
             request.form.get('banner_image', ''), request.form['venue_id'])
        )
        venue = query_db('SELECT total_capacity FROM VENUE WHERE venue_id=?', (request.form['venue_id'],), one=True)
        generate_seats_for_event(eid, venue['total_capacity'])
        flash('Event created successfully! Now add ticket types.', 'success')
        return redirect(url_for('edit_ticket_types', event_id=eid))
    return render_template('admin/event_form.html', venues=venues, event=None, user=current_user())

@app.route('/admin/events/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    event = query_db('SELECT * FROM EVENT WHERE event_id=?', (event_id,), one=True)
    venues = query_db('SELECT * FROM VENUE ORDER BY venue_name')
    if not event: abort(404)
    if request.method == 'POST':
        execute_db(
            'UPDATE EVENT SET event_name=?, event_date=?, event_time=?, description=?, category=?, event_status=?, banner_image=?, venue_id=? WHERE event_id=?',
            (request.form['event_name'], request.form['event_date'], request.form['event_time'],
             request.form['description'], request.form['category'], request.form['event_status'],
             request.form.get('banner_image', ''), request.form['venue_id'], event_id)
        )
        flash('Event updated successfully.', 'success')
        return redirect(url_for('admin_events'))
    return render_template('admin/event_form.html', venues=venues, event=event, user=current_user())

@app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
@admin_required
def delete_event(event_id):
    bookings = query_db('SELECT COUNT(*) as cnt FROM BOOKING WHERE event_id=? AND booking_status="Confirmed"', (event_id,), one=True)
    if bookings['cnt'] > 0:
        flash('Cannot delete event with confirmed bookings. Cancel bookings first.', 'danger')
    else:
        execute_db('DELETE FROM EVENT WHERE event_id=?', (event_id,))
        flash('Event deleted.', 'info')
    return redirect(url_for('admin_events'))

@app.route('/admin/events/<int:event_id>/tickets', methods=['GET', 'POST'])
@admin_required
def edit_ticket_types(event_id):
    event = query_db('SELECT * FROM EVENT WHERE event_id=?', (event_id,), one=True)
    if request.method == 'POST':
        names = request.form.getlist('type_name[]')
        prices = request.form.getlist('price[]')
        qtys = request.form.getlist('total_quantity[]')
        benefits = request.form.getlist('benefits[]')
        execute_db('DELETE FROM TICKET_TYPE WHERE event_id=?', (event_id,))
        for n, p, q, b in zip(names, prices, qtys, benefits):
            if n.strip():
                execute_db(
                    'INSERT INTO TICKET_TYPE (type_name, price, total_quantity, available_quantity, benefits, event_id) VALUES (?,?,?,?,?,?)',
                    (n.strip(), float(p), int(q), int(q), b.strip(), event_id)
                )
        flash('Ticket types saved.', 'success')
        return redirect(url_for('admin_events'))
    tickets = query_db('SELECT * FROM TICKET_TYPE WHERE event_id=?', (event_id,))
    return render_template('admin/ticket_types.html', event=event, tickets=tickets, user=current_user())

@app.route('/admin/venues')
@admin_required
def admin_venues():
    venues = query_db('SELECT v.*, (SELECT COUNT(*) FROM EVENT e WHERE e.venue_id=v.venue_id) as event_count FROM VENUE v ORDER BY v.venue_name')
    return render_template('admin/venues.html', venues=venues, user=current_user())

@app.route('/admin/venues/create', methods=['GET', 'POST'])
@admin_required
def create_venue():
    if request.method == 'POST':
        execute_db(
            'INSERT INTO VENUE (venue_name, address, total_capacity, amenities) VALUES (?,?,?,?)',
            (request.form['venue_name'], request.form['address'], int(request.form['total_capacity']), request.form['amenities'])
        )
        flash('Venue created successfully.', 'success')
        return redirect(url_for('admin_venues'))
    return render_template('admin/venue_form.html', venue=None, user=current_user())

@app.route('/admin/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_venue(venue_id):
    venue = query_db('SELECT * FROM VENUE WHERE venue_id=?', (venue_id,), one=True)
    if not venue: abort(404)
    if request.method == 'POST':
        execute_db(
            'UPDATE VENUE SET venue_name=?, address=?, total_capacity=?, amenities=? WHERE venue_id=?',
            (request.form['venue_name'], request.form['address'], int(request.form['total_capacity']), request.form['amenities'], venue_id)
        )
        flash('Venue updated.', 'success')
        return redirect(url_for('admin_venues'))
    return render_template('admin/venue_form.html', venue=venue, user=current_user())

@app.route('/admin/venues/<int:venue_id>/delete', methods=['POST'])
@admin_required
def delete_venue(venue_id):
    events = query_db('SELECT COUNT(*) as cnt FROM EVENT WHERE venue_id=?', (venue_id,), one=True)
    if events['cnt'] > 0:
        flash('Cannot delete venue with associated events.', 'danger')
    else:
        execute_db('DELETE FROM VENUE WHERE venue_id=?', (venue_id,))
        flash('Venue deleted.', 'info')
    return redirect(url_for('admin_venues'))

# ============================================================
# MODULE 2 & 3: SEAT & BOOKING MANAGEMENT
# ============================================================
@app.route('/event/<int:event_id>/seats')
@login_required
def seat_selection(event_id):
    event = query_db('SELECT e.*, v.venue_name FROM EVENT e JOIN VENUE v ON e.venue_id=v.venue_id WHERE e.event_id=?', (event_id,), one=True)
    if not event: abort(404)
    seats = query_db('SELECT * FROM SEAT WHERE event_id=? ORDER BY seat_row, seat_number', (event_id,))
    ticket_types = query_db('SELECT * FROM TICKET_TYPE WHERE event_id=? ORDER BY price DESC', (event_id,))
    seat_map = {}
    for s in seats:
        seat_map.setdefault(s['seat_row'], []).append(s)
    return render_template('seat_selection.html', event=event, seat_map=seat_map, ticket_types=ticket_types, user=current_user())

@app.route('/api/seats/<int:event_id>')
def get_seats(event_id):
    seats = query_db('SELECT * FROM SEAT WHERE event_id=?', (event_id,))
    return jsonify([dict(s) for s in seats])

@app.route('/booking/confirm', methods=['POST'])
@login_required
def confirm_booking():
    event_id = int(request.form['event_id'])
    seat_ids = [int(x) for x in request.form.get('seat_ids', '').split(',') if x]
    ticket_type_id = int(request.form['ticket_type_id'])
    if not seat_ids:
        flash('Please select at least one seat.', 'warning')
        return redirect(url_for('seat_selection', event_id=event_id))
    if len(seat_ids) > 10:
        flash('Maximum 10 seats per booking allowed.', 'warning')
        return redirect(url_for('seat_selection', event_id=event_id))
    ticket_type = query_db('SELECT * FROM TICKET_TYPE WHERE ticket_type_id=?', (ticket_type_id,), one=True)
    event = query_db('SELECT * FROM EVENT WHERE event_id=?', (event_id,), one=True)
    available_seats = query_db(
        f'SELECT * FROM SEAT WHERE seat_id IN ({",".join("?"*len(seat_ids))}) AND seat_status="Available" AND event_id=?',
        (*seat_ids, event_id)
    )
    if len(available_seats) != len(seat_ids):
        flash('Some seats are no longer available. Please try again.', 'danger')
        return redirect(url_for('seat_selection', event_id=event_id))
    unit_price = ticket_type['price']
    total_amount = unit_price * len(seat_ids)
    booking_ref = generate_ref('BK')
    hold_expiry = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
    booking_id = execute_db(
        'INSERT INTO BOOKING (booking_ref, customer_id, event_id, total_seats, total_amount, booking_status, temp_hold_expiry) VALUES (?,?,?,?,?,?,?)',
        (booking_ref, session['user_id'], event_id, len(seat_ids), total_amount, 'Pending', hold_expiry)
    )
    for s in available_seats:
        execute_db('UPDATE SEAT SET seat_status="Held" WHERE seat_id=?', (s['seat_id'],))
        execute_db(
            'INSERT INTO BOOKING_SEAT (booking_id, seat_id, ticket_type_id, unit_price) VALUES (?,?,?,?)',
            (booking_id, s['seat_id'], ticket_type_id, unit_price)
        )
    flash('Seats held for 10 minutes. Please complete payment.', 'info')
    return redirect(url_for('checkout', booking_id=booking_id))

@app.route('/checkout/<int:booking_id>')
@login_required
def checkout(booking_id):
    booking = query_db(
        'SELECT b.*, e.event_name, e.event_date, e.event_time, v.venue_name '
        'FROM BOOKING b JOIN EVENT e ON b.event_id=e.event_id JOIN VENUE v ON e.venue_id=v.venue_id '
        'WHERE b.booking_id=? AND b.customer_id=?', (booking_id, session['user_id']), one=True
    )
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('home'))
    if booking['booking_status'] != 'Pending':
        flash('This booking is not pending payment.', 'warning')
        return redirect(url_for('booking_detail', booking_id=booking_id))
    seats = query_db(
        'SELECT bs.*, s.seat_row, s.seat_number, s.seat_class, tt.type_name '
        'FROM BOOKING_SEAT bs JOIN SEAT s ON bs.seat_id=s.seat_id JOIN TICKET_TYPE tt ON bs.ticket_type_id=tt.ticket_type_id '
        'WHERE bs.booking_id=?', (booking_id,)
    )
    return render_template('checkout.html', booking=booking, seats=seats, user=current_user())

@app.route('/payment/process/<int:booking_id>', methods=['POST'])
@login_required
def process_payment(booking_id):
    booking = query_db('SELECT * FROM BOOKING WHERE booking_id=? AND customer_id=?', (booking_id, session['user_id']), one=True)
    if not booking or booking['booking_status'] != 'Pending':
        return jsonify({'success': False, 'message': 'Invalid booking'})
    payment_method = request.form.get('payment_method', 'Credit Card')
    success = random.random() > 0.1
    txn_id = generate_ref('TXN')
    if success:
        execute_db(
            'INSERT INTO PAYMENT (transaction_id, booking_id, payment_method, amount, payment_status, gateway_response) VALUES (?,?,?,?,?,?)',
            (txn_id, booking_id, payment_method, booking['total_amount'], 'Success', 'Gateway response: Payment OK')
        )
        execute_db('UPDATE BOOKING SET booking_status="Confirmed" WHERE booking_id=?', (booking_id,))
        execute_db(
            'UPDATE SEAT SET seat_status="Booked" WHERE seat_id IN (SELECT seat_id FROM BOOKING_SEAT WHERE booking_id=?)',
            (booking_id,)
        )
        bseats = query_db('SELECT ticket_type_id, COUNT(*) as cnt FROM BOOKING_SEAT WHERE booking_id=? GROUP BY ticket_type_id', (booking_id,))
        for bs in bseats:
            execute_db('UPDATE TICKET_TYPE SET available_quantity = available_quantity - ? WHERE ticket_type_id=?', (bs['cnt'], bs['ticket_type_id']))
        return jsonify({'success': True, 'message': 'Payment successful!', 'redirect': url_for('booking_detail', booking_id=booking_id)})
    else:
        execute_db(
            'INSERT INTO PAYMENT (transaction_id, booking_id, payment_method, amount, payment_status, gateway_response) VALUES (?,?,?,?,?,?)',
            (txn_id, booking_id, payment_method, booking['total_amount'], 'Failed', 'Gateway response: Insufficient funds / Timeout')
        )
        return jsonify({'success': False, 'message': 'Payment failed. Please try again.'})

@app.route('/booking/<int:booking_id>')
@login_required
def booking_detail(booking_id):
    booking = query_db(
        'SELECT b.*, e.event_name, e.event_date, e.event_time, e.description, v.venue_name, v.address, c.full_name, c.email, c.phone '
        'FROM BOOKING b JOIN EVENT e ON b.event_id=e.event_id JOIN VENUE v ON e.venue_id=v.venue_id JOIN CUSTOMER c ON b.customer_id=c.customer_id '
        'WHERE b.booking_id=?', (booking_id,), one=True
    )
    if not booking: abort(404)
    if session.get('user_role') != 'Admin' and booking['customer_id'] != session['user_id']:
        abort(403)
    seats = query_db(
        'SELECT bs.*, s.seat_row, s.seat_number, s.seat_class, tt.type_name, tt.price '
        'FROM BOOKING_SEAT bs JOIN SEAT s ON bs.seat_id=s.seat_id JOIN TICKET_TYPE tt ON bs.ticket_type_id=tt.ticket_type_id '
        'WHERE bs.booking_id=?', (booking_id,)
    )
    payment = query_db('SELECT * FROM PAYMENT WHERE booking_id=?', (booking_id,), one=True)
    refund = query_db('SELECT * FROM REFUND WHERE booking_id=?', (booking_id,), one=True)
    refund_estimate = None
    if booking['booking_status'] == 'Confirmed' and not refund:
        ref_amt, ref_policy = calculate_refund(booking['event_date'], booking['total_amount'])
        refund_estimate = {'amount': ref_amt, 'policy': ref_policy}
    return render_template('booking_detail.html', booking=booking, seats=seats, payment=payment, refund=refund, refund_estimate=refund_estimate, user=current_user())

@app.route('/bookings')
@login_required
def my_bookings():
    user_role = session.get('user_role')
    if user_role == 'Admin':
        bookings = query_db(
            'SELECT b.*, e.event_name, e.event_date, c.full_name, c.email FROM BOOKING b '
            'JOIN EVENT e ON b.event_id=e.event_id JOIN CUSTOMER c ON b.customer_id=c.customer_id '
            'ORDER BY b.booking_date DESC'
        )
    else:
        bookings = query_db(
            'SELECT b.*, e.event_name, e.event_date FROM BOOKING b JOIN EVENT e ON b.event_id=e.event_id '
            'WHERE b.customer_id=? ORDER BY b.booking_date DESC', (session['user_id'],)
        )
    return render_template('bookings.html', bookings=bookings, user=current_user())

# ============================================================
# MODULE 4: CANCELLATION & REFUND
# ============================================================
@app.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = query_db('SELECT * FROM BOOKING WHERE booking_id=?', (booking_id,), one=True)
    if not booking: abort(404)
    if session.get('user_role') != 'Admin' and booking['customer_id'] != session['user_id']:
        abort(403)
    if booking['booking_status'] != 'Confirmed':
        flash('Only confirmed bookings can be cancelled.', 'warning')
        return redirect(url_for('booking_detail', booking_id=booking_id))
    event = query_db('SELECT event_date FROM EVENT WHERE event_id=?', (booking['event_id'],), one=True)
    event_dt = datetime.strptime(event['event_date'], '%Y-%m-%d').date()
    hours_to_event = (datetime.combine(event_dt, datetime.min.time()) - datetime.now()).total_seconds() / 3600
    if hours_to_event < 24 and session.get('user_role') != 'Admin':
        flash('Cannot cancel within 24 hours of event. Contact admin for exceptions.', 'danger')
        return redirect(url_for('booking_detail', booking_id=booking_id))
    refund_amount, refund_reason = calculate_refund(event['event_date'], booking['total_amount'])
    refund_ref = generate_ref('RF')
    execute_db(
        'INSERT INTO REFUND (refund_ref, booking_id, refund_amount, refund_status, refund_reason, requested_at) VALUES (?,?,?,?,?,?)',
        (refund_ref, booking_id, refund_amount, 'Processing', refund_reason, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    execute_db('UPDATE BOOKING SET booking_status="Cancelled" WHERE booking_id=?', (booking_id,))
    execute_db(
        'UPDATE SEAT SET seat_status="Available" WHERE seat_id IN (SELECT seat_id FROM BOOKING_SEAT WHERE booking_id=?)',
        (booking_id,)
    )
    bseats = query_db('SELECT ticket_type_id, COUNT(*) as cnt FROM BOOKING_SEAT WHERE booking_id=? GROUP BY ticket_type_id', (booking_id,))
    for bs in bseats:
        execute_db('UPDATE TICKET_TYPE SET available_quantity = available_quantity + ? WHERE ticket_type_id=?', (bs['cnt'], bs['ticket_type_id']))
    execute_db('UPDATE PAYMENT SET payment_status="Refunded" WHERE booking_id=? AND payment_status="Success"', (booking_id,))
    flash(f'Booking cancelled. Refund of Rs.{refund_amount:.2f} initiated. {refund_reason}', 'success')
    return redirect(url_for('booking_detail', booking_id=booking_id))

@app.route('/admin/refunds/<int:refund_id>/process', methods=['POST'])
@admin_required
def process_refund(refund_id):
    refund = query_db('SELECT * FROM REFUND WHERE refund_id=?', (refund_id,), one=True)
    if not refund: abort(404)
    execute_db(
        'UPDATE REFUND SET refund_status="Completed", processed_at=? WHERE refund_id=?',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), refund_id)
    )
    flash('Refund processed successfully.', 'success')
    return redirect(url_for('admin_refunds'))

@app.route('/admin/refunds')
@admin_required
def admin_refunds():
    refunds = query_db(
        'SELECT r.*, b.booking_ref, e.event_name, c.full_name, c.email FROM REFUND r '
        'JOIN BOOKING b ON r.booking_id=b.booking_id JOIN EVENT e ON b.event_id=e.event_id JOIN CUSTOMER c ON b.customer_id=c.customer_id '
        'ORDER BY r.requested_at DESC'
    )
    return render_template('admin/refunds.html', refunds=refunds, user=current_user())

@app.route('/admin/customers')
@admin_required
def admin_customers():
    customers = query_db(
        'SELECT c.*, (SELECT COUNT(*) FROM BOOKING b WHERE b.customer_id=c.customer_id) as booking_count '
        'FROM CUSTOMER c ORDER BY c.created_at DESC'
    )
    return render_template('admin/customers.html', customers=customers, user=current_user())

# ============================================================
# ADMIN DASHBOARD
# ============================================================
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_events = query_db('SELECT COUNT(*) as cnt FROM EVENT', one=True)['cnt']
    total_bookings = query_db('SELECT COUNT(*) as cnt FROM BOOKING WHERE booking_status="Confirmed"', one=True)['cnt']
    total_revenue = query_db('SELECT COALESCE(SUM(amount),0) as total FROM PAYMENT WHERE payment_status="Success"', one=True)['total']
    total_customers = query_db('SELECT COUNT(*) as cnt FROM CUSTOMER WHERE user_role="Customer"', one=True)['cnt']
    recent_bookings = query_db(
        'SELECT b.*, e.event_name, c.full_name FROM BOOKING b JOIN EVENT e ON b.event_id=e.event_id JOIN CUSTOMER c ON b.customer_id=c.customer_id '
        'ORDER BY b.booking_date DESC LIMIT 10'
    )
    sales_data = query_db(
        'SELECT DATE(p.payment_date) as dt, SUM(p.amount) as amt FROM PAYMENT p WHERE p.payment_status="Success" '
        'GROUP BY DATE(p.payment_date) ORDER BY dt DESC LIMIT 10'
    )
    event_sales = query_db(
        'SELECT e.event_name, COUNT(b.booking_id) as bookings, COALESCE(SUM(b.total_amount),0) as revenue '
        'FROM EVENT e LEFT JOIN BOOKING b ON e.event_id=b.event_id AND b.booking_status="Confirmed" '
        'GROUP BY e.event_id ORDER BY revenue DESC LIMIT 5'
    )
    return render_template('admin/dashboard.html', user=current_user(),
        total_events=total_events, total_bookings=total_bookings,
        total_revenue=total_revenue, total_customers=total_customers,
        recent_bookings=recent_bookings, sales_data=list(reversed(sales_data)),
        event_sales=event_sales)

# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user()), 404

@app.errorhandler(403)
def forbidden(e):
    flash('Access denied.', 'danger')
    return redirect(url_for('home')), 403

# ============================================================
# INIT & RUN
# ============================================================
if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print('Initializing database...')
        init_db()
    else:
        conn = get_db()
        try:
            conn.execute('SELECT COUNT(*) FROM EVENT')
            conn.close()
        except Exception:
            conn.close()
            print('Database missing tables, reinitializing...')
            init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
