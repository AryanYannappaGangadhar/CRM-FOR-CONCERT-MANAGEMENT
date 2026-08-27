-- ============================================================
-- ONLINE EVENT TICKET BOOKING SYSTEM
-- Database Schema (SQLite Compatible)
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLE: VENUE
-- ============================================================
CREATE TABLE IF NOT EXISTS VENUE (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT NOT NULL,
    address TEXT NOT NULL,
    total_capacity INTEGER NOT NULL CHECK (total_capacity > 0),
    amenities TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT CHK_VENUE_CAPACITY CHECK (total_capacity > 0)
);

-- ============================================================
-- TABLE: EVENT
-- ============================================================
CREATE TABLE IF NOT EXISTS EVENT (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    description TEXT DEFAULT '',
    category TEXT NOT NULL DEFAULT 'Other',
    event_status TEXT NOT NULL DEFAULT 'Draft',
    banner_image TEXT DEFAULT '',
    venue_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT CHK_EVENT_STATUS CHECK (event_status IN ('Draft','Published','Sold Out','Completed','Cancelled')),
    CONSTRAINT CHK_EVENT_CATEGORY CHECK (category IN ('Concert','Conference','Sports','Theater','Workshop','Other')),
    CONSTRAINT FK_EVENT_VENUE FOREIGN KEY (venue_id) REFERENCES VENUE(venue_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_EVENT_VENUE ON EVENT(venue_id);
CREATE INDEX IF NOT EXISTS IDX_EVENT_DATE ON EVENT(event_date, event_status);
CREATE INDEX IF NOT EXISTS IDX_EVENT_CATEGORY ON EVENT(category);

-- ============================================================
-- TABLE: CUSTOMER
-- ============================================================
CREATE TABLE IF NOT EXISTS CUSTOMER (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    address TEXT DEFAULT '',
    user_role TEXT NOT NULL DEFAULT 'Customer',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT CHK_USER_ROLE CHECK (user_role IN ('Customer','Admin'))
);

-- ============================================================
-- TABLE: TICKET_TYPE
-- ============================================================
CREATE TABLE IF NOT EXISTS TICKET_TYPE (
    ticket_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0.0,
    total_quantity INTEGER NOT NULL DEFAULT 0,
    available_quantity INTEGER NOT NULL DEFAULT 0,
    benefits TEXT DEFAULT '',
    event_id INTEGER NOT NULL,
    CONSTRAINT CHK_TICKET_PRICE CHECK (price >= 0),
    CONSTRAINT FK_TICKETTYPE_EVENT FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_TICKET_EVENT ON TICKET_TYPE(event_id);

-- ============================================================
-- TABLE: SEAT
-- ============================================================
CREATE TABLE IF NOT EXISTS SEAT (
    seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    seat_row TEXT NOT NULL,
    seat_number TEXT NOT NULL,
    seat_class TEXT NOT NULL DEFAULT 'Standard',
    seat_status TEXT NOT NULL DEFAULT 'Available',
    event_id INTEGER NOT NULL,
    CONSTRAINT CHK_SEAT_STATUS CHECK (seat_status IN ('Available','Held','Booked','Blocked')),
    CONSTRAINT CHK_SEAT_CLASS CHECK (seat_class IN ('VIP','Premium','Standard','Economy')),
    CONSTRAINT UK_SEAT_EVENT_ROW_NUM UNIQUE (event_id, seat_row, seat_number),
    CONSTRAINT FK_SEAT_EVENT FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_SEAT_EVENT ON SEAT(event_id);
CREATE INDEX IF NOT EXISTS IDX_SEAT_STATUS ON SEAT(event_id, seat_status);

-- ============================================================
-- TABLE: BOOKING
-- ============================================================
CREATE TABLE IF NOT EXISTS BOOKING (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_ref TEXT NOT NULL UNIQUE,
    customer_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    total_seats INTEGER NOT NULL DEFAULT 0,
    total_amount REAL NOT NULL DEFAULT 0.0,
    booking_status TEXT NOT NULL DEFAULT 'Pending',
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    temp_hold_expiry DATETIME,
    CONSTRAINT CHK_BOOKING_STATUS CHECK (booking_status IN ('Pending','Confirmed','Cancelled','Failed')),
    CONSTRAINT CHK_TOTAL_AMOUNT CHECK (total_amount >= 0),
    CONSTRAINT FK_BOOKING_CUSTOMER FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FK_BOOKING_EVENT FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_BOOKING_CUST ON BOOKING(customer_id);
CREATE INDEX IF NOT EXISTS IDX_BOOKING_EVENT ON BOOKING(event_id);
CREATE INDEX IF NOT EXISTS IDX_BOOKING_REF ON BOOKING(booking_ref);
CREATE INDEX IF NOT EXISTS IDX_BOOKING_STATUS ON BOOKING(booking_status, booking_date);
CREATE INDEX IF NOT EXISTS IDX_BOOKING_EVENT_DATE ON BOOKING(event_id, booking_date, booking_status);

-- ============================================================
-- TABLE: BOOKING_SEAT
-- ============================================================
CREATE TABLE IF NOT EXISTS BOOKING_SEAT (
    booking_seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    ticket_type_id INTEGER NOT NULL,
    unit_price REAL NOT NULL DEFAULT 0.0,
    CONSTRAINT FK_BOOKINGSEAT_BOOKING FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_BOOKINGSEAT_SEAT FOREIGN KEY (seat_id) REFERENCES SEAT(seat_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FK_BOOKINGSEAT_TICKETTYPE FOREIGN KEY (ticket_type_id) REFERENCES TICKET_TYPE(ticket_type_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_BKS_BOOKING ON BOOKING_SEAT(booking_id);
CREATE INDEX IF NOT EXISTS IDX_BKS_SEAT ON BOOKING_SEAT(seat_id);

-- ============================================================
-- TABLE: PAYMENT
-- ============================================================
CREATE TABLE IF NOT EXISTS PAYMENT (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT NOT NULL UNIQUE,
    booking_id INTEGER NOT NULL UNIQUE,
    payment_method TEXT NOT NULL,
    amount REAL NOT NULL DEFAULT 0.0,
    payment_status TEXT NOT NULL DEFAULT 'Pending',
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    gateway_response TEXT DEFAULT '',
    CONSTRAINT CHK_PAYMENT_METHOD CHECK (payment_method IN ('Credit Card','Debit Card','UPI','Net Banking','Wallet')),
    CONSTRAINT CHK_PAYMENT_STATUS CHECK (payment_status IN ('Pending','Success','Failed','Refunded')),
    CONSTRAINT CHK_PAYMENT_AMOUNT CHECK (amount >= 0),
    CONSTRAINT FK_PAYMENT_BOOKING FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_PAYMENT_BOOKING ON PAYMENT(booking_id);

-- ============================================================
-- TABLE: REFUND
-- ============================================================
CREATE TABLE IF NOT EXISTS REFUND (
    refund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    refund_ref TEXT NOT NULL UNIQUE,
    booking_id INTEGER NOT NULL UNIQUE,
    refund_amount REAL NOT NULL DEFAULT 0.0,
    refund_status TEXT NOT NULL DEFAULT 'Initiated',
    refund_reason TEXT DEFAULT '',
    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME,
    CONSTRAINT CHK_REFUND_STATUS CHECK (refund_status IN ('Initiated','Processing','Completed','Failed','Rejected')),
    CONSTRAINT CHK_REFUND_AMOUNT CHECK (refund_amount >= 0),
    CONSTRAINT FK_REFUND_BOOKING FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS IDX_REFUND_BOOKING ON REFUND(booking_id);

-- ============================================================
-- SEED DATA: INSERT DEFAULT ADMIN USER
-- Password: admin123 (hashed using werkzeug)
-- ============================================================
INSERT OR IGNORE INTO CUSTOMER (customer_id, full_name, email, phone, password_hash, address, user_role)
VALUES (1, 'System Administrator', 'admin@ticketbook.com', '+91-9876543210',
        'pbkdf2:sha256:260000$adminhashedpassword$8c8f9c7b6a5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8',
        'Head Office, Corporate Park', 'Admin');

-- ============================================================
-- SEED DATA: SAMPLE VENUES
-- ============================================================
INSERT OR IGNORE INTO VENUE (venue_id, venue_name, address, total_capacity, amenities) VALUES
(1, 'Grand Arena', '123 Main Street, Downtown', 2000, 'Parking, AC, Food Court, VIP Lounge'),
(2, 'City Convention Center', '456 Business Ave', 800, 'Conference Rooms, Projector, WiFi, Catering'),
(3, 'Sports Complex', '789 Stadium Rd', 5000, 'Open Air, Floodlights, Dressing Rooms, Food Stalls'),
(4, 'Royal Theater', '321 Cultural Lane', 500, 'Proscenium Stage, Orchestral Pit, Balcony Seating, AC');

-- ============================================================
-- SEED DATA: SAMPLE EVENTS
-- ============================================================
INSERT OR IGNORE INTO EVENT (event_id, event_name, event_date, event_time, description, category, event_status, banner_image, venue_id) VALUES
(1, 'Summer Music Festival', '2026-09-15', '18:00:00', 'Join us for an evening of live music featuring top artists from around the world. Three stages, non-stop entertainment!', 'Concert', 'Published', '/static/images/event1.jpg', 1),
(2, 'Tech Summit 2026', '2026-10-05', '09:00:00', 'The largest technology conference of the year. Keynotes, workshops, and networking with industry leaders.', 'Conference', 'Published', '/static/images/event2.jpg', 2),
(3, 'Cricket Championship Finals', '2026-09-28', '14:00:00', 'Witness the epic final showdown between the top two teams. Dont miss the excitement!', 'Sports', 'Published', '/static/images/event3.jpg', 3),
(4, 'Shakespeare: Hamlet', '2026-10-20', '19:30:00', 'A timeless classic brought to life by award-winning actors. A must-see for theater enthusiasts.', 'Theater', 'Published', '/static/images/event4.jpg', 4),
(5, 'Data Science Workshop', '2026-09-20', '10:00:00', 'Hands-on workshop covering machine learning, deep learning, and AI applications. Beginner to Intermediate level.', 'Workshop', 'Published', '/static/images/event5.jpg', 2);

-- ============================================================
-- SEED DATA: SAMPLE TICKET TYPES
-- ============================================================
INSERT OR IGNORE INTO TICKET_TYPE (ticket_type_id, type_name, price, total_quantity, available_quantity, benefits, event_id) VALUES
(1, 'VIP Pass', 2999.00, 200, 200, 'VIP Lounge Access, Front Row, Free Food & Drinks, Artist Meet', 1),
(2, 'Premium', 1499.00, 600, 600, 'Premium Seating, Food Coupon Worth Rs.200', 1),
(3, 'Standard', 799.00, 1200, 1200, 'General Admission, Seat Selection', 1),
(4, 'Delegate Pass', 4999.00, 100, 100, 'All Sessions, Workshop Access, Conference Kit, Lunch, Networking Dinner', 2),
(5, 'Standard Pass', 2499.00, 400, 400, 'Main Sessions Only, Conference Kit, Lunch', 2),
(6, 'Student Pass', 1299.00, 300, 300, 'Main Sessions, Lunch (Valid ID Required)', 2),
(7, 'VIP Box', 7499.00, 50, 50, 'Private Box, Catering Included, Parking Pass', 3),
(8, 'Premium Stand', 1499.00, 1000, 1000, 'Premium View, Food Coupons', 3),
(9, 'General Stand', 499.00, 3950, 3950, 'General Viewing Area', 3),
(10, 'Premium', 2499.00, 100, 100, 'Orchestra Seating, Program Booklet', 4),
(11, 'Standard', 1299.00, 250, 250, 'Balcony/Stall Seating', 4),
(12, 'Pro Ticket', 3499.00, 30, 30, 'Laptop Included, Dataset Access, Certificate, Lunch, Post-Workshop Support', 5),
(13, 'Standard Ticket', 1499.00, 120, 120, 'Certificate, Lunch, Study Material', 5);

-- ============================================================
-- SEED DATA: SAMPLE CUSTOMERS
-- ============================================================
INSERT OR IGNORE INTO CUSTOMER (customer_id, full_name, email, phone, password_hash, address, user_role) VALUES
(2, 'Rajesh Kumar', 'rajesh@email.com', '+91-9812345678', 'pbkdf2:sha256:260000$customerhashed1$a1b2c3d4e5f6', '101 Park View Apartments', 'Customer'),
(3, 'Priya Sharma', 'priya@email.com', '+91-9988776655', 'pbkdf2:sha256:260000$customerhashed2$f6e5d4c3b2a1', '202 Green Towers', 'Customer'),
(4, 'Amit Patel', 'amit@email.com', '+91-9123456789', 'pbkdf2:sha256:260000$customerhashed3$9f8e7d6c5b4a', '303 Blue Residency', 'Customer');
