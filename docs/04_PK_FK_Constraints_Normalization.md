# DATABASE DESIGN DOCUMENT
## Online Event Ticket Booking System
### 9. PK & FK Constraints | 10. Normalization

---

## 9. PRIMARY KEY & FOREIGN KEY CONSTRAINTS

### 9.1 Primary Key (PK) Definitions

Each table has a surrogate key (auto-increment integer) as its Primary Key for simplicity and performance.

| Table | Primary Key | Type | Constraint Name | Notes |
|-------|-------------|------|-----------------|-------|
| **VENUE** | `venue_id` | INT AUTO_INCREMENT | PK_VENUE | Clustered index |
| **EVENT** | `event_id` | INT AUTO_INCREMENT | PK_EVENT | Clustered index |
| **TICKET_TYPE** | `ticket_type_id` | INT AUTO_INCREMENT | PK_TICKET_TYPE | Clustered index |
| **SEAT** | `seat_id` | INT AUTO_INCREMENT | PK_SEAT | Clustered index |
| **CUSTOMER** | `customer_id` | INT AUTO_INCREMENT | PK_CUSTOMER | Clustered index |
| **BOOKING** | `booking_id` | INT AUTO_INCREMENT | PK_BOOKING | Clustered index |
| **BOOKING_SEAT** | `booking_seat_id` | INT AUTO_INCREMENT | PK_BOOKING_SEAT | Clustered index |
| **PAYMENT** | `payment_id` | INT AUTO_INCREMENT | PK_PAYMENT | Clustered index |
| **REFUND** | `refund_id` | INT AUTO_INCREMENT | PK_REFUND | Clustered index |

### 9.2 Unique Key (UK) / Candidate Key Definitions

| Table | Unique Key | Reason |
|-------|-----------|--------|
| CUSTOMER | `email` | Each customer must have unique email |
| BOOKING | `booking_ref` | Human-readable unique booking reference (e.g., BK20260001) |
| PAYMENT | `transaction_id` | Unique gateway transaction ID |
| REFUND | `refund_ref` | Unique refund reference number |
| SEAT | `(event_id, seat_row, seat_number)` | Composite unique: same seat number per event |

### 9.3 Foreign Key (FK) Constraints with Referential Actions

```sql
-- ============================================================
-- FOREIGN KEY CONSTRAINTS (Referential Integrity Rules)
-- ============================================================

-- RULE: EVENT.VENUE_ID references VENUE.VENUE_ID
-- ON DELETE: RESTRICT  (cannot delete venue if events exist)
-- ON UPDATE: CASCADE   (if venue_id changes, update in events)
ALTER TABLE EVENT ADD CONSTRAINT FK_EVENT_VENUE
    FOREIGN KEY (venue_id) REFERENCES VENUE(venue_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- RULE: TICKET_TYPE.EVENT_ID references EVENT.EVENT_ID
-- ON DELETE: CASCADE   (deleting event removes its ticket types)
-- ON UPDATE: CASCADE
ALTER TABLE TICKET_TYPE ADD CONSTRAINT FK_TICKETTYPE_EVENT
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- RULE: SEAT.EVENT_ID references EVENT.EVENT_ID
-- ON DELETE: CASCADE   (deleting event removes all its seats)
-- ON UPDATE: CASCADE
ALTER TABLE SEAT ADD CONSTRAINT FK_SEAT_EVENT
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- RULE: BOOKING.CUSTOMER_ID references CUSTOMER.CUSTOMER_ID
-- ON DELETE: RESTRICT  (cannot delete customer with bookings)
-- ON UPDATE: CASCADE
ALTER TABLE BOOKING ADD CONSTRAINT FK_BOOKING_CUSTOMER
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- RULE: BOOKING.EVENT_ID references EVENT.EVENT_ID
-- ON DELETE: RESTRICT  (cannot delete event with bookings)
-- ON UPDATE: CASCADE
ALTER TABLE BOOKING ADD CONSTRAINT FK_BOOKING_EVENT
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- RULE: BOOKING_SEAT.BOOKING_ID references BOOKING.BOOKING_ID
-- ON DELETE: CASCADE   (deleting booking removes its seat records)
-- ON UPDATE: CASCADE
ALTER TABLE BOOKING_SEAT ADD CONSTRAINT FK_BOOKINGSEAT_BOOKING
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- RULE: BOOKING_SEAT.SEAT_ID references SEAT.SEAT_ID
-- ON DELETE: RESTRICT  (seat should not be deleted if referenced)
-- ON UPDATE: CASCADE
ALTER TABLE BOOKING_SEAT ADD CONSTRAINT FK_BOOKINGSEAT_SEAT
    FOREIGN KEY (seat_id) REFERENCES SEAT(seat_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- RULE: BOOKING_SEAT.TICKET_TYPE_ID references TICKET_TYPE.TICKET_TYPE_ID
-- ON DELETE: RESTRICT
-- ON UPDATE: CASCADE
ALTER TABLE BOOKING_SEAT ADD CONSTRAINT FK_BOOKINGSEAT_TICKETTYPE
    FOREIGN KEY (ticket_type_id) REFERENCES TICKET_TYPE(ticket_type_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- RULE: PAYMENT.BOOKING_ID references BOOKING.BOOKING_ID
-- ON DELETE: CASCADE
-- ON UPDATE: CASCADE
ALTER TABLE PAYMENT ADD CONSTRAINT FK_PAYMENT_BOOKING
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- RULE: REFUND.BOOKING_ID references BOOKING.BOOKING_ID
-- ON DELETE: CASCADE
-- ON UPDATE: CASCADE
ALTER TABLE REFUND ADD CONSTRAINT FK_REFUND_BOOKING
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
```

### 9.4 CHECK Constraints (Domain Integrity)

```sql
-- EVENT STATUS CHECK
ALTER TABLE EVENT ADD CONSTRAINT CHK_EVENT_STATUS
    CHECK (event_status IN ('Draft', 'Published', 'Sold Out', 'Completed', 'Cancelled'));

-- EVENT CATEGORY CHECK
ALTER TABLE EVENT ADD CONSTRAINT CHK_EVENT_CATEGORY
    CHECK (category IN ('Concert', 'Conference', 'Sports', 'Theater', 'Workshop', 'Other'));

-- SEAT STATUS CHECK
ALTER TABLE SEAT ADD CONSTRAINT CHK_SEAT_STATUS
    CHECK (seat_status IN ('Available', 'Held', 'Booked', 'Blocked'));

-- SEAT CLASS CHECK
ALTER TABLE SEAT ADD CONSTRAINT CHK_SEAT_CLASS
    CHECK (seat_class IN ('VIP', 'Premium', 'Standard', 'Economy'));

-- BOOKING STATUS CHECK
ALTER TABLE BOOKING ADD CONSTRAINT CHK_BOOKING_STATUS
    CHECK (booking_status IN ('Pending', 'Confirmed', 'Cancelled', 'Failed'));

-- USER ROLE CHECK
ALTER TABLE CUSTOMER ADD CONSTRAINT CHK_USER_ROLE
    CHECK (user_role IN ('Customer', 'Admin'));

-- PAYMENT METHOD CHECK
ALTER TABLE PAYMENT ADD CONSTRAINT CHK_PAYMENT_METHOD
    CHECK (payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Wallet'));

-- PAYMENT STATUS CHECK
ALTER TABLE PAYMENT ADD CONSTRAINT CHK_PAYMENT_STATUS
    CHECK (payment_status IN ('Pending', 'Success', 'Failed', 'Refunded'));

-- REFUND STATUS CHECK
ALTER TABLE REFUND ADD CONSTRAINT CHK_REFUND_STATUS
    CHECK (refund_status IN ('Initiated', 'Processing', 'Completed', 'Failed', 'Rejected'));

-- POSITIVE AMOUNT CHECKS
ALTER TABLE TICKET_TYPE ADD CONSTRAINT CHK_TICKET_PRICE CHECK (price >= 0);
ALTER TABLE BOOKING ADD CONSTRAINT CHK_TOTAL_AMOUNT CHECK (total_amount >= 0);
ALTER TABLE PAYMENT ADD CONSTRAINT CHK_PAYMENT_AMOUNT CHECK (amount >= 0);
ALTER TABLE REFUND ADD CONSTRAINT CHK_REFUND_AMOUNT CHECK (refund_amount >= 0);
```

---

## 10. NORMALIZATION

### 10.1 Normalization Goal
Achieve **Boyce-Codd Normal Form (BCNF)** with 3NF as minimum to eliminate:
- Insertion Anomalies
- Updation Anomalies  
- Deletion Anomalies
- Data Redundancy

---

### UNF (Unnormalized Form) - Initial State
```
Customer(customer_id, name, email, phone, bookings_list[event_name, event_date, seats_booked, amount_paid])
```
**Problem:** Multi-valued attribute (bookings_list), repeating groups.

---

### 1NF (First Normal Form) - Eliminate Repeating Groups
**Rule:** Each cell must contain atomic value; each record unique.

**Step:** Remove repeating group into separate table.
```
CUSTOMER(customer_id, name, email, phone, address, password_hash, role)
BOOKING(booking_id, booking_ref, customer_id, event_name, event_date, total_seats, total_amount)
```

**Anomaly still present:** Event details (event_name, event_date) repeated for every booking of same event.

---

### 2NF (Second Normal Form) - Remove Partial Dependencies
**Rule:** Must be in 1NF + All non-key attributes fully functionally dependent on entire PK (no partial dependencies).

**Step:** Split out event attributes into EVENT table.
```
EVENT(event_id PK, event_name, event_date, event_time, description, category)
CUSTOMER(customer_id PK, name, email, phone, address, password_hash, role)
BOOKING(booking_id PK, booking_ref, customer_id FK, event_id FK, total_seats, total_amount)
```

**Now in 2NF:** All non-key attributes depend on full PK.  
**Anomaly still present:** Venue details missing, seat-per-booking not tracked.

---

### 3NF (Third Normal Form) - Remove Transitive Dependencies
**Rule:** Must be in 2NF + No transitive dependencies (non-key attributes depend only on PK, not on other non-key attributes).

**Step:** Add VENUE table (venue details only depend on venue, not event). Create SEAT, BOOKING_SEAT, PAYMENT, REFUND tables.

```
VENUE(venue_id PK, venue_name, address, total_capacity, amenities)

EVENT(event_id PK, event_name, event_date, event_time, description, category, event_status, venue_id FK)
  - Transitive dependency removed: venue moved to VENUE table

TICKET_TYPE(ticket_type_id PK, type_name, price, total_qty, event_id FK)

SEAT(seat_id PK, seat_row, seat_number, seat_class, seat_status, event_id FK)

CUSTOMER(customer_id PK, full_name, email UK, phone, password_hash, address, user_role)

BOOKING(booking_id PK, booking_ref UK, customer_id FK, event_id FK, total_seats, total_amount, booking_status)

BOOKING_SEAT(booking_seat_id PK, booking_id FK, seat_id FK, ticket_type_id FK, unit_price)
  - Resolves M:N between BOOKING and SEAT

PAYMENT(payment_id PK, transaction_id UK, booking_id FK, payment_method, amount, payment_status)
  - 1:1 with BOOKING, separated to avoid NULLs for pending bookings

REFUND(refund_id PK, refund_ref UK, booking_id FK, refund_amount, refund_status)
  - 1:0..1 with BOOKING, separated to avoid NULLs for non-refunded bookings
```

**Check 3NF Transitive Dependencies:**
- ❌ Transitive: If venue_name was in EVENT → would depend on venue_id, not event_id
- ✅ Fixed: venue_name is in VENUE, event only has venue_id FK

---

### BCNF (Boyce-Codd Normal Form) - Stronger 3NF
**Rule:** For every non-trivial functional dependency X → Y, X must be a superkey.

**Verification for each table:**

| Table | Functional Dependencies | Is Determinant a Superkey? | BCNF? |
|-------|-------------------------|---------------------------|-------|
| VENUE | venue_id → all attrs | Yes (PK) | ✅ Yes |
| EVENT | event_id → all attrs | Yes (PK) | ✅ Yes |
| TICKET_TYPE | ticket_type_id → all attrs | Yes (PK) | ✅ Yes |
| SEAT | seat_id → all attrs; (event_id, row, num) → seat_id | Yes (both are superkeys) | ✅ Yes |
| CUSTOMER | customer_id → all; email → customer_id | Yes (PK + UK) | ✅ Yes |
| BOOKING | booking_id → all; booking_ref → booking_id | Yes | ✅ Yes |
| BOOKING_SEAT | booking_seat_id → all; (booking_id, seat_id) → booking_seat_id | Yes | ✅ Yes |
| PAYMENT | payment_id → all; transaction_id → all; booking_id → payment_id | Yes | ✅ Yes |
| REFUND | refund_id → all; refund_ref → all; booking_id → refund_id | Yes | ✅ Yes |

**Conclusion:** All tables are in **BCNF**. No anomalies present.

---

### 10.2 Denormalization Considerations (For Performance)
While schema is in BCNF, for production we might introduce:
1. **Materialized View:** `event_sales_summary` (sum of bookings per event) - avoids joins on dashboard
2. **Redundant column:** `EVENT.total_bookings` counter - cached aggregate (updated via triggers)
3. **Indexing strategy:** Composite indexes on frequent query columns

---

### 10.3 Index Strategy (For Query Performance)

```sql
-- Primary Keys are automatically indexed (clustered)

-- Foreign Keys (indexed for fast joins)
CREATE INDEX IDX_EVENT_VENUE     ON EVENT(venue_id);
CREATE INDEX IDX_TICKET_EVENT    ON TICKET_TYPE(event_id);
CREATE INDEX IDX_SEAT_EVENT      ON SEAT(event_id);
CREATE INDEX IDX_BOOKING_CUST    ON BOOKING(customer_id);
CREATE INDEX IDX_BOOKING_EVENT   ON BOOKING(event_id);
CREATE INDEX IDX_BKS_BOOKING     ON BOOKING_SEAT(booking_id);
CREATE INDEX IDX_BKS_SEAT        ON BOOKING_SEAT(seat_id);
CREATE INDEX IDX_PAYMENT_BOOKING ON PAYMENT(booking_id);
CREATE INDEX IDX_REFUND_BOOKING  ON REFUND(booking_id);

-- Frequent Search Columns
CREATE INDEX IDX_EVENT_DATE      ON EVENT(event_date, event_status);
CREATE INDEX IDX_EVENT_CATEGORY  ON EVENT(category);
CREATE INDEX IDX_CUST_EMAIL      ON CUSTOMER(email);   -- Email is UK, auto-indexed in most DBs
CREATE INDEX IDX_BOOKING_REF     ON BOOKING(booking_ref);
CREATE INDEX IDX_BOOKING_STATUS  ON BOOKING(booking_status, booking_date);
CREATE INDEX IDX_SEAT_STATUS     ON SEAT(event_id, seat_status);

-- Composite Index for Reports
CREATE INDEX IDX_BOOKING_EVENT_DATE ON BOOKING(event_id, booking_date, booking_status);
```

---

*Document Version: 1.0 | Database: SQLite / PostgreSQL Compatible*
