# TESTING DOCUMENTATION
## Online Event Ticket Booking System
### 11. Test Plan | 12. Test Cases (20+) | 13. Black-Box | 14. White-Box | 15. System Testing

---

## 11. TEST PLAN

### 11.1 Test Plan Introduction
This document outlines the testing strategy, test cases, and test results for the Online Event Ticket Booking System. The goal is to ensure all functional and non-functional requirements are met with a defect rate < 5%.

### 11.2 Scope of Testing
| Test Level | Scope |
|------------|-------|
| Unit Testing | Individual functions, DB queries, utility methods |
| Integration Testing | Module interactions, Database ↔ App ↔ UI layer |
| System Testing | End-to-end scenarios covering all 4 modules |
| Black-Box Testing | Functionality without internal knowledge (input/output) |
| White-Box Testing | Code paths, branches, edge cases in Flask routes |
| Security Testing | Auth, session, SQL injection, XSS vectors |
| UI/UX Testing | Responsive design, cross-browser compatibility |
| Performance Testing | Page load, concurrent bookings, seat locking |

### 11.3 Test Schedule & Resources
| Activity | Duration | Resources |
|----------|----------|-----------|
| Test Planning | 1 day | Test Lead |
| Test Case Design | 2 days | QA Team |
| Environment Setup | 0.5 day | DevOps |
| Test Execution | 3 days | QA Team |
| Defect Reporting & Fixing | 2 days | Dev + QA |
| Regression Testing | 1 day | QA Team |
| UAT Sign-off | 0.5 day | Stakeholders |

### 11.4 Test Environment
- **OS:** Windows 10 / Ubuntu 20.04
- **Browser:** Chrome 120+, Firefox 120+, Edge 120+
- **Backend:** Python 3.9, Flask 2.3
- **Database:** SQLite 3.40+
- **RAM:** 4GB minimum, 8GB recommended
- **Screen Resolutions:** 1920x1080, 1366x768, 375x667 (mobile)

### 11.5 Entry & Exit Criteria
**Entry Criteria:**
- Build is deployed on test environment
- Smoke test cases pass
- All modules coded and unit tested
- Test data prepared

**Exit Criteria:**
- 100% test cases executed
- Critical & High severity defects fixed & closed
- No open "Blocker" defects
- Regression test pass rate ≥ 95%
- UAT sign-off obtained

### 11.6 Defect Classification
| Severity | Description | Example |
|----------|-------------|---------|
| **Blocker (P0)** | System unusable, no workaround | App crash on booking |
| **Critical (P1)** | Core feature broken | Double booking same seat |
| **Major (P2)** | Non-critical feature broken | Filter not working |
| **Minor (P3)** | Cosmetic / usability issue | Button misalignment |
| **Trivial (P4)** | Very minor | Typo in label |

### 11.7 Testing Tools
| Tool | Purpose |
|------|---------|
| Selenium / Playwright | Automated UI testing (E2E) |
| pytest / unittest | Python unit testing framework |
| Postman | API testing (REST endpoints) |
| JMeter | Performance / Load testing |
| OWASP ZAP | Security vulnerability scanning |
| Chrome DevTools | Debugging, mobile simulation |
| Manual Testing | Exploratory, UX, ad-hoc testing |

---

## 12. TEST CASES (20+)

### TEST CASE TEMPLATE:
| TC ID | Module | Test Scenario | Test Steps | Test Data | Expected Result | Actual Result | Status | Severity |
|-------|--------|---------------|------------|-----------|-----------------|---------------|--------|----------|

---

### MODULE 2: CUSTOMER MANAGEMENT (Authentication)

| ID | Test Scenario | Steps | Data | Expected Result |
|----|---------------|-------|------|-----------------|
| **TC-01** | Customer Registration - Valid Data | 1. Navigate to /register<br>2. Fill all fields with valid data<br>3. Click Create Account | Name: Test User<br>Email: test@test.com<br>Phone: 9999999999<br>Pass: test@123 | Registration successful, redirect to homepage, session created, user in DB |
| **TC-02** | Registration - Duplicate Email | 1. Register with an existing email<br>2. Submit form | Email: admin@ticketbook.com | Error: "Email already registered." No duplicate created |
| **TC-03** | Registration - Weak Password | 1. Enter password < 6 chars<br>2. Submit | Pass: "abc" | Error: "Password must be at least 6 characters." |
| **TC-04** | Login - Valid Credentials | 1. Navigate to /login<br>2. Enter valid email & pass | Email: admin@ticketbook.com<br>Pass: admin123 | Login successful → Dashboard/Home, session created |
| **TC-05** | Login - Invalid Password | 1. Enter correct email, wrong password<br>2. Submit | Pass: "wrongpass123" | Error: "Invalid email or password." No session created |
| **TC-06** | Logout Functionality | 1. Login as any user<br>2. Click Logout link | - | Session destroyed, redirect to home, logged out state visible |
| **TC-07** | Protected Route - Unauthenticated Access | 1. Without login, visit /profile, /booking/1, /checkout/1 | - | Redirect to /login page with flash message |
| **TC-08** | Admin Route - Customer Access | 1. Login as Customer<br>2. Visit /admin/dashboard | - | Flash: "Admin access required." → Redirected home |

---

### MODULE 1: EVENT & VENUE MANAGEMENT

| ID | Test Scenario | Steps | Data | Expected Result |
|----|---------------|-------|------|-----------------|
| **TC-09** | Admin Create Venue | 1. Login as Admin → Venues → Create<br>2. Fill venue details → Save | Name: "Mini Hall", Capacity: 100, Address: "Test Address" | Venue created in DB, appears in list, total count +1 |
| **TC-10** | Delete Venue with Events | 1. Try delete a venue that has events | Existing venue with ≥1 event | Error: "Cannot delete venue with associated events." Delete prevented |
| **TC-11** | Create Event & Associate Venue | 1. Admin → Events → Create<br>2. Fill all event fields, select venue<br>3. Save | Event: "Test Event", Date: future, Venue: existing one | Event created, seats auto-generated (based on venue capacity), ticket type page shown |
| **TC-12** | Event Status Update | 1. Edit event, change status from Draft → Published<br>2. Visit homepage (non-admin view) | - | Event appears on /home page in Published events list |
| **TC-13** | Event Search & Filter | 1. On homepage, enter search keyword<br>2. Select category filter | Keyword: "Music", Category: "Concert" | Only matching events shown. Filter + Search work together |
| **TC-14** | Define Ticket Types for Event | 1. Open event → Ticket Types<br>2. Add 3 types (VIP/Premium/Standard) with prices/qty | VIP: Rs.3000, Premium: Rs.1500, Standard: Rs.800 | 3 rows inserted into TICKET_TYPE table. Event detail page shows all types |

---

### MODULE 3: SEAT & BOOKING MANAGEMENT

| ID | Test Scenario | Steps | Data | Expected Result |
|----|---------------|-------|------|-----------------|
| **TC-15** | Seat Map Display & Selection | 1. Open event → Seat Selection<br>2. Click 3 available seats | Seats A1, A2, A3 (Available class) | Seats highlight as selected, summary updates (3 seats × unit price) |
| **TC-16** | Prevent Overbooking Same Seat | 1. User-A books seat B5 (confirms payment)<br>2. User-B tries to select same seat B5 | Seat B5 | Step 2: Seat B5 shows as "Booked" (gray) → unclickable. Prevents double booking |
| **TC-17** | Exceed 10 Seat Max | 1. In seat selection, select 11 seats | 11 seats clicked | Alert: "Maximum 10 seats per booking allowed." 11th seat rejected |
| **TC-18** | Temporary Seat Hold (10 min) | 1. Select seats & proceed to checkout (seats → Held)<br>2. Without paying, wait timeout | - | After 10 min, seats revert to Available. DB: seat_status = Available, booking_status = (stays Pending or can be Failed) |
| **TC-19** | Create Booking - Happy Path | 1. Login → Select event → Select seats → Proceed<br>2. At checkout, pay successfully | 2 seats, Rs.1500 each = Rs.3000 | Unique booking_ref generated. DB: BOOKING row (status=Confirmed), BOOKING_SEAT rows, SEAT status=Booked, PAYMENT row (Success). Customer receives confirmation |

---

### MODULE 4: PAYMENT, CANCELLATION & REFUND

| ID | Test Scenario | Steps | Data | Expected Result |
|----|---------------|-------|------|-----------------|
| **TC-20** | Payment - Failure & Retry | 1. At checkout, trigger a failed payment<br>2. Click "Try Again" & succeed | - | Step 1: PAYMENT status=Failed, seats still held. Step 2: 2nd PAYMENT row status=Success, Booking Confirmed |
| **TC-21** | Calculate Refund - >7 days before event | 1. For confirmed booking (event >7 days away)<br>2. Click Cancel | Total=Rs.3000, event in 10 days | Refund estimate: Rs.3000 (100%). On confirm: Booking=Cancelled, Refund=Initiated, seats=Available |
| **TC-22** | Calculate Refund - 3-7 days before event | 1. Confirmed booking, event in 5 days | Total=Rs.3000 | Refund estimate: Rs.1500 (50%) |
| **TC-23** | Calculate Refund - <3 days before event | 1. Confirmed booking, event in 2 days | Total=Rs.3000 | Refund estimate: Rs.0 (No refund) |
| **TC-24** | Cancel Booking Within 24 Hours of Event | 1. Try cancel booking with event <24 hours | - | Error: "Cannot cancel within 24 hours of event." |
| **TC-25** | Admin Process Refund | 1. Customer cancelled (Refund=Processing)<br>2. Admin → Refunds → Process button | - | Refund → Completed, processed_at timestamp set. Email/SMS sent (simulated) |
| **TC-26** | Seat Inventory Restored After Cancellation | 1. Book 2 seats → booking confirmed<br>2. Cancel booking | 2 VIP seats A10, A11 | Step 2: After cancel, SEAT.status = Available. TICKET_TYPE.available_quantity increases by 2 |

---

### NON-FUNCTIONAL & SECURITY TEST CASES

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| **TC-27** | SQL Injection Check | Login form: Enter email = `' OR '1'='1` | Login fails (no SQLi). Parameterized queries protect DB |
| **TC-28** | XSS Attack Prevention | Register with Name: `<script>alert(1)</script>` | Name stored in escaped form. UI renders text, JS does not execute |
| **TC-29** | Concurrent Users (50+) | Simulate 50 users trying to book remaining 40 seats | Only 40 succeed, 10 fail with "seats not available". No double booking |
| **TC-30** | Page Load Time Performance | Load /home page on 4G connection | DOM Load < 3 seconds, as per NFR-01.1 |
| **TC-31** | Mobile Responsiveness | Open app on 375x667 viewport | All elements responsive, navbar collapses, seat map scrolls, no horizontal scroll |
| **TC-32** | Database Integrity - FK Constraint | Try to create EVENT with non-existent venue_id (99999) | SQLite: FOREIGN KEY constraint failed. Event not created. |

---

## 13. BLACK-BOX TESTING

### 13.1 Black-Box Testing Overview
Black-box testing verifies system functionality **without examining internal code/logic**. Testers only see inputs and outputs. Focuses on: requirements coverage, boundary values, invalid inputs, user workflows.

**Techniques Used:**
1. **Equivalence Partitioning (EP)**
2. **Boundary Value Analysis (BVA)**
3. **Decision Table Testing**
4. **State Transition Testing**
5. **Error Guessing**

---

### 13.2 Equivalence Partitioning Examples

| Test Field | Valid Partitions | Invalid Partitions |
|------------|------------------|--------------------|
| **Customer Name** | 2-100 alphabet chars (spaces allowed) | 0, 1 chars; >100 chars; numbers/special chars only |
| **Email** | valid@domain.tld format | No @, No domain, Double dots, Spaces |
| **Password** | 6-50 chars, any mix | <6 chars, Empty, >100 chars |
| **Ticket Price** | 0 to 99999 (0=Free event) | Negative, >99999, text input |
| **Seats per Booking** | 1, 2, ... 10 seats | 0 seats, 11+ seats |
| **Phone Number** | 10-15 digits, +,- allowed | <10 digits, letters |

### 13.3 Boundary Value Analysis (BVA) for Key Fields

| Field | Min-1 | Min | Normal | Max | Max+1 |
|-------|-------|-----|--------|-----|-------|
| Password Length | 5 ❌ | 6 ✅ | 12 ✅ | 50 ✅ | 51 ❌ (truncated or rejected) |
| Seats per Booking | 0 ❌ | 1 ✅ | 5 ✅ | 10 ✅ | 11 ❌ (alert shown) |
| Ticket Price (Rs.) | -1 ❌ | 0 ✅ (Free) | 500 ✅ | 99999 ✅ | 100000+ ⚠️ |
| Event Capacity | 0 ❌ | 1 ✅ | 500 ✅ | 100000 ✅ | Large allowed (perf impact) |

### 13.4 Decision Table: Refund Calculation Logic

**Rules:**
| Condition | R1 | R2 | R3 | R4 |
|-----------|----|----|----|----|
| Days before event > 7? | Y | N | N | N |
| Days before event 3-7? | - | Y | N | N |
| Days before event < 3? | - | - | Y | N |
| Within 24 hours (Admin override only) | - | - | - | Y |
| **Action: Refund %** | **100%** | **50%** | **0%** | **Block Cancel** |
| Allow cancellation? | Yes | Yes | Yes (No refund) | No (unless Admin) |

### 13.5 State Transition Diagram - Booking States
```
PENDING → (pay success) → CONFIRMED → (customer cancel) → CANCELLED
  │                            │
  │                            └── (event date passes) → COMPLETED
  └── (time-out / pay fail) → FAILED
```
**Test Transitions:**
- PENDING → CONFIRMED: Verify successful payment, seats → Booked
- PENDING → FAILED: Verify failed payment, seats → Available
- CONFIRMED → CANCELLED: Verify seats → Available, refund row created
- CANCELLED → CONFIRMED: Negative test, should not transition back

### 13.6 Sample Black-Box Test Cases
| BB-TC | Input | Expected Output | Technique |
|-------|-------|-----------------|-----------|
| BB-01 | Password length: 5 chars | Error: "≥ 6 chars" | BVA Min-1 |
| BB-02 | Select 10 seats → 11th seat click | Alert: Max 10 allowed | BVA Max+1 |
| BB-03 | Event 1 day away, customer cancel | Cancel blocked, "24hr" error | Decision R4 |
| BB-04 | Email: `notanemail` | Invalid email format error | EP Invalid |
| BB-05 | Search for nonexistent event "xyzzy" | Empty state, "No events found" | Error Guessing |

---

## 14. WHITE-BOX TESTING

### 14.1 White-Box Testing Overview
White-box (structural) testing designs test cases based on **internal code structure, logic paths, branches, and data flow**. Requires knowledge of Flask app routes and database queries.

**Techniques Used:**
1. **Statement Coverage** - Every line of code executed at least once
2. **Branch/Decision Coverage** - Every `if/else` branch taken True and False
3. **Path Coverage** - Independent paths through functions tested
4. **Condition Coverage** - Each sub-condition evaluated True/False
5. **Loop Testing** - Zero, 1, many iterations

**Target Coverage:**
| Metric | Target |
|--------|--------|
| Statement Coverage | ≥ 80% |
| Branch Coverage | ≥ 85% |
| Critical Module Coverage (Booking/Payment) | ≥ 95% |

---

### 14.2 Code-Based Test Cases (Route: /confirm_booking)

**Code snippet pseudocode:**
```python
FUNCTION confirm_booking:
  1: seat_ids = parse form input
  2: IF seat_ids empty → flash error, REDIRECT seat_selection
  3: IF len(seat_ids) > 10 → flash error, REDIRECT
  4: available_seats = SELECT seats WHERE status='Available' AND seat_id IN seat_ids
  5: IF len(available_seats) != len(seat_ids) → flash some seats booked ERROR, REDIRECT
  6: ELSE:
      6a: Create BOOKING (status=Pending, hold=10min)
      6b: UPDATE each seat → status='Held'
      6c: INSERT BOOKING_SEAT rows
  7: REDIRECT checkout
```

**White-box paths to test (McCabe Cyclomatic Complexity: 5):**
| WB-TC | Path | Input | Branches Covered |
|-------|------|-------|------------------|
| WB-01 | Lines 1→2→return | empty seat_ids | 2=True |
| WB-02 | Lines 1→2→3→return | 11 seat IDs | 2=False, 3=True |
| WB-03 | Lines 1→2→3→4→5→return | 5 IDs, one already Booked | 2=False, 3=False, 5=True |
| WB-04 | Lines 1→2→3→4→5→6→7 return | 4 valid available seats | 2=False, 3=False, 5=False, 6 all statements |

---

### 14.3 Branch Coverage: Cancel Booking Logic
```python
IF booking_status != 'Confirmed': ERROR-A
ELSE:
    hours_to_event = calculate()
    IF hours_to_event < 24 AND role != 'Admin': ERROR-B
    ELSE:
        calculate refund()
        IF days > 7 → refund 100%
        ELIF days >= 3 → refund 50%
        ELSE → 0%
```
| WB-TC | Scenario | Branches Hit |
|-------|----------|--------------|
| WB-05 | Cancel Pending booking | ERROR-A (True) |
| WB-06 | Cancel Confirmed, >7 days, Customer | ERROR-A F, ERROR-B F, days>7 T |
| WB-07 | Cancel Confirmed, 5 days, Customer | days>7 F, days>=3 T → 50% |
| WB-08 | Cancel Confirmed, 2 days, Customer | days>7 F, days>=3 F → 0% |
| WB-09 | Cancel Confirmed, 12 hours, **Admin** | ERROR-B F (Admin override), 0% refund |
| WB-10 | Cancel Confirmed, 12 hours, Customer | ERROR-B T (Blocked) |

---

### 14.4 Database Query Testing (Data Flow)
| WB-TC | Query / Scenario | Test Method |
|-------|------------------|-------------|
| WB-11 | `get_seats(event_id)` - Validate JOIN & FK | Verify only seats of that event returned; seat_status values correct |
| WB-12 | `DELETE EVENT` with existing bookings (ON DELETE RESTRICT) | Should raise IntegrityError; event preserved |
| WB-13 | `DELETE EVENT` with no bookings (CASCADE tickets/seats) | Check TICKET_TYPE, SEAT rows auto-deleted |
| WB-14 | Booking transaction rollback on exception | Inject error mid-booking; no half-filled tables (ACID) |
| WB-15 | Password hashing `check_password()` | Same password → True; wrong password → False; hash != plaintext |

---

### 14.5 Loop Testing - Seat Map Generation
```python
FOR each row in rows:  # rows from A-Z
    FOR each seat in 1..15:
        INSERT SEAT
```
| WB-TC | Loop Type | Test |
|-------|-----------|------|
| WB-16 | Outer FOR zero | Venue capacity 1 → 1 row, 1 seat |
| WB-17 | Outer FOR one | Capacity 15 → 1 row, 15 seats |
| WB-18 | Outer FOR many | Capacity 5000 → ~334 rows, inner 15 each, last row partial |

---

## 15. SYSTEM TESTING

### 15.1 System Testing Overview
System testing verifies the **complete, integrated system** against all functional and non-functional requirements. All 4 modules tested as a whole in an environment that mirrors production.

### 15.2 End-to-End (E2E) Business Flows

#### E2E-01: Complete Happy Path - Event Booking Lifecycle
```
Pre-requisite: Admin has created event (with venue & ticket types)
```
| Step | Actor | Action | Expected |
|------|-------|--------|----------|
| 1 | Admin | Login as admin@ticketbook.com | Dashboard shows stats |
| 2 | Admin | Create Venue "Hall A" → capacity 50 | Venue added |
| 3 | Admin | Create Event "Rock Fest 2026" + assign "Hall A" | Event created, 50 seats auto-generated |
| 4 | Admin | Add Ticket Types: Standard (Rs.500, 50 qty) | 1 ticket type saved |
| 5 | Customer | Register new user "Ravi" | Account created, logged in |
| 6 | Customer | Browse events → "Rock Fest 2026" | Event detail shows ticket types |
| 7 | Customer | Seat Selection → pick 4 seats (A1-A4) → checkout | 4 seats Held, booking Pending |
| 8 | Customer | Complete payment with Credit Card | Payment Success, booking → Confirmed |
| 9 | Customer | Visit Booking Detail page | Shows confirmed status, e-ticket, 4 seats listed |
| 10 | Admin | Dashboard → see booking count updated | Stats: bookings +1, revenue + Rs.2000 |
| 11 | Customer | Request Cancel (event is 10 days away) | Cancel success → Refund Rs.2000 (100%), seats Released |
| 12 | Admin | Refunds page → click Process | Refund status → Completed |
| **PASS CRITERIA** | - | - | All 12 steps succeed. DB: BOOKING row → Cancelled, REFUND row → Completed, 4 seats → Available again |

---

#### E2E-02: Multiple Users Seat Concurrency
| Step | Actor | Action | Expected |
|------|-------|--------|----------|
| 1 | Setup | Event has 1 remaining seat: Z-15 | DB: 1 seat Available |
| 2 | Customer-A (Browser 1) | Select seat Z-15 → Checkout page | Seat Held by A |
| 3 | Customer-B (Browser 2) | Load seat map for same event | Seat Z-15 shows as "Held" (cannot select) |
| 4 | Customer-A | Abandons checkout (wait 10 min) | Seat Z-15 → Available again |
| 5 | Customer-B | Refreshes → selects Z-15 → Pays & Confirms | Success! Only B got the seat. No double booking. |

---

#### E2E-03: Admin Event CRUD + Revenue Check
| Step | Action | Verification |
|------|--------|--------------|
| 1 | Create 2 events → 10 tickets each @ Rs.1000 | 2 events visible |
| 2 | Book 6 tickets for Event-1, 4 tickets for Event-2 | BOOKING rows created |
| 3 | Admin Dashboard | Revenue = 10 × 1000 = Rs.10,000. Event-1 = 60%, Event-2 = 40% |
| 4 | Cancel 2 tickets from Event-1 | Revenue = 8000. 2 seats available |
| 5 | Delete Event-2 (4 bookings → error) | Can't delete event with bookings. ✅ |
| 6 | Cancel all Event-2 bookings, then delete event | Event-2 deleted, dashboard revenue updated |

---

### 15.3 Non-Functional System Tests

| System Test ID | Category | Test Procedure | Requirement Verified | Pass/Fail Criterion |
|----------------|----------|----------------|----------------------|---------------------|
| ST-PERF-01 | Performance | Measure /home load time with 500 events cached | NFR-01.1 Page Load ≤ 3s | T < 3s → Pass |
| ST-PERF-02 | Performance | Submit 100 concurrent booking requests | NFR-01.7 ≥ 100 bookings/minute | Throughput ≥ target |
| ST-SEC-01 | Security | Submit login form with SQL injection payloads | NFR-02.4 SQL injection protection | No DB data leakage |
| ST-SEC-02 | Security | Post script tag in event description / user name | NFR-02.5 XSS Protection | Sanitized output, no alert |
| ST-SEC-03 | Security | Customer URL-manipulate /admin/... path | NFR-02.7 RBAC Admin check | Redirect + denied |
| ST-REL-01 | Reliability | Run 1000 successful bookings through the system | NFR-03.2 MTBF ≥ 100h | 0 crashes / failures |
| ST-REL-02 | Reliability | Kill app mid-transaction → restart | NFR-03.5 ACID compliance | No partial bookings |
| ST-COMP-01 | Compatibility | Full happy path on Chrome, Firefox, Edge, Safari | NFR-05.1 Browser compat list | Works on all 4 |
| ST-COMP-02 | Compatibility | Full happy path on iPhone SE (375x667) + iPad | NFR-05.2 Mobile responsive | All actions usable |
| ST-USAB-01 | Usability | New user completes booking without help docs | NFR-04.1 No training needed | Success rate ≥ 90% |

---

### 15.4 System Testing - Summary Report (Sample)
| Test Suite | Total TC | Passed | Failed | Blocked | Pass % |
|------------|----------|--------|--------|---------|--------|
| Authentication (TC-01 to 08) | 8 | 8 | 0 | 0 | 100% |
| Event/Venue Mgmt (TC-09 to 14) | 6 | 6 | 0 | 0 | 100% |
| Seat & Booking Mgmt (TC-15 to 19) | 5 | 5 | 0 | 0 | 100% |
| Payment, Cancel, Refund (TC-20 to 26) | 7 | 7 | 0 | 0 | 100% |
| Security & NFR (TC-27 to 32) | 6 | 6 | 0 | 0 | 100% |
| **TOTAL** | **32** | **32** | **0** | **0** | **100%** |

---

*Document Version: 1.0 | Testing Document - All 17 Deliverables Completed*
