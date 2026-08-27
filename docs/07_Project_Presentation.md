# PROJECT PRESENTATION
## Online Event Ticket Booking System
### Software Engineering Project Submission

**To be used as slide deck content (20 Slides)**

---

---

## SLIDE 1: TITLE SLIDE

**🎟️ Online Event Ticket Booking System**

**Software Engineering Project**

| Presented By: | Group Members |
|---|---|
| Course | Software Engineering |
| Submission Date | August 2026 |
| Technology Stack | Python · Flask · SQLite · Bootstrap 5 · JavaScript |

---

## SLIDE 2: AGENDA

📋 Today's Presentation Outline:

1. **Project Overview & Problem Statement** - Why build this?
2. **Objectives & Scope** - What's included vs excluded
3. **4 Core Modules** - Feature walkthrough
4. **System Architecture** - 3-Tier design + Tech Stack
5. **Database Design** - ER Diagram, 9 Tables, BCNF Normalization
6. **UML Diagrams** - Use Case Diagram, key scenarios
7. **Demo** - Live working application (8 key screens)
8. **Testing Strategy** - 32 Test Cases, Black/White/System Testing
9. **Challenges & Learnings**
10. **Future Enhancements & Conclusion**

---

## SLIDE 3: PROBLEM STATEMENT

⚠️ **Why Traditional Ticketing Fails:**

| Problem | Impact |
|---------|--------|
| 🐌 **Manual Process** | Long queues, errors, venue visit required |
| ❌ **No Real-Time Seats** | Double booking, customer disputes |
| 🌐 **Limited Accessibility** | Only during business hours, in-person only |
| 💰 **Refund Delays** | Cash-based, 7-14 day processing |
| 📊 **No Data Visibility** | Organizers can't forecast demand or trends |
| 💥 **Peak Time Failures** | Systems crash during popular launches |

✅ **Our Solution:** A fully automated, web-based, real-time event ticketing platform that solves all 6 problems.

---

## SLIDE 4: OBJECTIVES

🎯 **What We Set Out to Achieve**

### Primary (5):
1. **Web platform** for browsing & booking event tickets
2. **Real-time seat map** with visual selection
3. **Admin tools** to manage events, venues, tickets
4. **Multi-method payments** with instant confirmations
5. **Automated cancellation & tiered refunds**

### Secondary (5):
6. Customer profiles with booking history
7. Admin analytics & sales reports
8. Secure role-based authentication (Admin/Customer)
9. **Fully responsive** UI (Mobile → Desktop)
10. **BCNF Normalized** database with integrity constraints

---

## SLIDE 5: SCOPE - INCLUDED vs EXCLUDED

✅ **IN SCOPE (Delivered All 4 Modules):**
- **Module 1:** Event CRUD, Venue CRUD, Categories, Status Workflow
- **Module 2:** Registration/Login/Profile, Ticket Types, Printable E-Tickets
- **Module 3:** Interactive seat map, 10-min hold, max 10 seat rule, concurrency safe
- **Module 4:** 5 payment methods, 3-tier refund engine, seat restore on cancel

❌ **OUT OF SCOPE (Future Roadmap):**
- Physical ticket shipping
- Virtual event / live streaming
- Multi-language / Multi-currency
- Social media marketing integration
- Accounting software sync

---

## SLIDE 6: SYSTEM ARCHITECTURE

🏗️ **3-Tier Client-Server Architecture**

```
┌────────────────────────────────────────────┐
│ PRESENTATION TIER  (User's Browser)        │
│ HTML5 · CSS3 · Bootstrap 5 · JavaScript    │
│ Chart.js · Responsive Grid · Print CSS     │
└──────────────────┬─────────────────────────┘
                   │ HTTPS / JSON APIs
┌──────────────────▼─────────────────────────┐
│ APPLICATION TIER   (Flask / Python 3.9)    │
│ 4 Module Controllers · 32 Routes           │
│ Auth Decorators · Session Management       │
│ Business Logic · Refund Engine             │
└──────────────────┬─────────────────────────┘
                   │ Parameterized SQL queries
┌──────────────────▼─────────────────────────┐
│ DATA TIER     (SQLite 3.x)                 │
│ 9 Tables · BCNF Compliant                  │
│ PK/UK/FK/CHECK Constraints · 12+ Indexes   │
│ ACID Transactions · Referential Integrity  │
└────────────────────────────────────────────┘
```

---

## SLIDE 7: TECHNOLOGY STACK

🛠️ **Tools & Why We Chose Them**

| Layer | Technology | Why? |
|-------|------------|------|
| **Frontend** | HTML5 + CSS3 + Bootstrap 5 | Fastest responsive UI, 12-col grid, polished components |
| **Frontend** | JavaScript (ES6) + Chart.js | Client-side validation, dashboard graphs |
| **Backend** | Python 3.9 + Flask 2.3 | Minimal, powerful, great for academic projects |
| **Security** | Werkzeug (bcrypt-style) | Industry-standard password hashing |
| **Database** | SQLite 3.x | Zero-config, file-based, full FK/ACID support |
| **Diagrams** | Mermaid.js | Text-based ER/UML → renders in Markdown viewers |
| **Testing** | pytest-compatible (manual TCs executed) | 32 Test Cases, 100% pass |

---

## SLIDE 8: MODULE 1 - EVENT & VENUE MANAGEMENT

📅 **Module 1: Event & Venue Management**

**Admin-only module. Everything CRUD:**

### Venue Management:
- 🏟️ Venue record (name, address, capacity, amenities)
- 🚫 **Delete protection:** Cannot delete venue with active events
- Auto-generates seats when event is created

### Event Management:
- 🎤 Full CRUD with categories: Concert / Conference / Sports / Theater / Workshop / Other
- 📊 Status lifecycle: Draft → Published → Sold Out → Completed / Cancelled
- 🎟️ Event ↔ Venue mapping
- 📢 Homepage: Search + Category filter chips

> **Demo Screens:** Admin Venue List → Admin Event Form → Ticket Type Editor → Customer Event Detail

---

## SLIDE 9: MODULE 2 - CUSTOMER & TICKET MANAGEMENT

👥 **Module 2: Customer & Ticket Management**

### Customer System:
- 📝 Registration with unique email validation
- 🔐 Secure login (bcrypt password hashing + sessions)
- 👤 Profile page: Personal info + Booking stats (spent, confirmed count)
- 🎭 Roles: Customer / Admin (RBAC everywhere)

### Ticket System:
- 🎫 Multi-tier ticket types per event (VIP, Premium, Standard, Early Bird...)
- 💰 Configurable price + quantity + benefits per tier
- 🖨️ **Digital E-Ticket:** QR visual + Booking Ref + Seats + Customer info + Venue instructions
- 🖨️ **Print CSS:** Hides nav/buttons when printed

---

## SLIDE 10: MODULE 3 - SEAT & BOOKING MANAGEMENT

💺 **Module 3: Seat & Booking Management - The "Heart"**

### Interactive Seat Map:
- 🎭 Stage header + Rows A-Z × Seats 1-15 grid
- 🎨 **4 Visual states:** 🟢 Available 🔵 Selected ⚪ Booked 🟡 Held
- 💎 Seat class coloring: VIP=Pink, Premium=Purple, Standard=Green
- 📊 Running total sidebar: Selected seats list × Unit price = Total

### Concurrency & Safety:
- ⏱️ **10-min temporary hold** (JS countdown on checkout page)
- 🎯 **10-seat max** per booking (JS + backend double-check)
- 🛡️ **Atomic SELECT + UPDATE pattern** prevents double-booking (Tested with 2 concurrent users)
- 📝 Unique Booking Ref: BK + YYYYMMDD + 6 digits

---

## SLIDE 11: MODULE 4 - PAYMENT, CANCELLATION & REFUND

💳 **Module 4: Payment, Cancellation & Refund**

### Payment System:
- 5 Methods: 💳 Credit · 💳 Debit · 📱 UPI · 🏦 Net Banking · 👛 Wallet
- ✅ 90% success simulator (tests failure path too)
- 📝 Full audit log: transaction ID + method + status + gateway response
- 🧾 Payment Receipt data visible in booking detail

### Cancellation & Refund Engine (3-Tier Rule):
| When Canceled | Refund % | Policy |
|---|---|---|
| 📅 **> 7 days before** | 100% ✅ | Full refund |
| 📅 **3-7 days before** | 50% ⚠️ | Half refund |
| 📅 **< 3 days before** | 0% ❌ | No refund |

### Safety:
- 🚫 **24-hour hard block** for customers (Admin override allowed)
- 🔄 Cancelled seats → **instantly restored** to available inventory
- 📈 Ticket quantity counter restored automatically

---

## SLIDE 12: DATABASE DESIGN OVERVIEW

💾 **Schema: 9 Tables - BCNF Compliant**

```
VENUE (1) ── hosts ──→ (N) EVENT (N) ── has ──→ (N) TICKET_TYPE
                         │
                         ├── contains ──→ (N) SEAT
                         │
CUSTOMER (1) ── makes ──→ (N) BOOKING (N) ── includes via BOOKING_SEAT ──→ (N) SEAT
                              │                          │
                              │ assigned via              └─ assigned as ──→ TICKET_TYPE
                              1 : 1
                              │
                              ▼
                           PAYMENT
                              │
                              0..1 : 1
                              ▼
                           REFUND
```

### Integrity:
✓ 9 Primary Keys · ✓ 5 Unique Keys · ✓ 10 Foreign Keys  
✓ 15 CHECK Constraints (status enums, non-negative amounts)  
✓ 12 Performance Indexes

---

## SLIDE 13: PK & FK CONSTRAINTS + NORMALIZATION

🔗 **Referential Integrity (Cascade vs Restrict)**

**Table: EVENT → VENUE**
```sql
FOREIGN KEY (venue_id) REFERENCES VENUE(venue_id)
  ON DELETE RESTRICT   -- Can't delete venue with events!
  ON UPDATE CASCADE
```

**Table: BOOKING → CUSTOMER**
```sql
FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
  ON DELETE RESTRICT   -- Can't delete customer with bookings!
```

**Table: EVENT → SEAT**
```sql
FOREIGN KEY (event_id) REFERENCES EVENT(event_id)
  ON DELETE CASCADE    -- Delete event → delete all seats (if no bookings)
```

### 🎯 Normalization: BCNF Achieved
- 1NF ✓ Atomic values, no repeating groups
- 2NF ✓ Full functional dependency on PK (no partial)
- 3NF ✓ No transitive (venue moved to own table; not stored in event)
- **BCNF ✓ Every FD's Left-Hand-Side is a Superkey**

---

## SLIDE 14: UML DIAGRAM - USE CASES

👤 **Actors: Customer · Admin · Payment Gateway · Email Service**

**Customer Use Cases (14):**
Register · Login · Manage Profile · Browse Events · Search/Filter · View Event Details  
Select Seats · Hold Seats · Create Booking · Modify Booking · Process Payment  
Cancel Booking · Request Refund · Track Refund · Download E-Ticket

**Admin Use Cases (8):**
Login · Manage Events CRUD · Manage Venues CRUD · Define Ticket Types  
View Sales Reports · Manage All Bookings · Override Refunds · Manage Customers

**Includes / Extends:**
- Process Payment ✕ **includes** → Payment Gateway
- Create Booking ✕ **includes** → Temporarily Hold Seats
- Cancel Booking ✕ **includes** → Calculate & Request Refund
- Create Booking ✕ **includes** → Send Email Confirmation

---

## SLIDE 15: TESTING STRATEGY

🧪 **Testing - 32 Test Cases, 100% Pass Rate**

### Distribution:
| Module | # TCs | Pass |
|---|---|---|
| Authentication | 8 | 8/8 |
| Event & Venue Mgmt | 6 | 6/6 |
| Seat & Booking Mgmt | 5 | 5/5 |
| Payment / Cancel / Refund | 7 | 7/7 |
| Security & NFR | 6 | 6/6 |
| **TOTAL** | **32** | **32/32** |

### Techniques Used:
**🖤 Black-Box:** Equivalence Partitioning · BVA · Decision Table (Refund) · State Transition (Booking states)  
**🤍 White-Box:** Statement/Branch/Loop coverage · Path testing (5 paths in confirm_booking)  
**💻 System Testing:** 3 full E2E flows · NFR (perf, security, compatibility)

---

## SLIDE 16: SECURITY TESTING RESULTS

🔒 **Security - All Tests Passed**

| Test | Attack / Payload | Result |
|---|---|---|
| **SQL Injection** | `' OR '1'='1` in login email | ✅ BLOCKED - parameterized queries → no result |
| **XSS Stored** | `<script>alert(1)</script>` in name | ✅ BLOCKED - Jinja2 auto-escapes output |
| **IDOR / BOLA** | Customer visits /admin/dashboard | ✅ BLOCKED - `admin_required` decorator |
| **IDOR #2** | Customer tries another user's `/booking/999` | ✅ BLOCKED - ownership check in route |
| **Brute Force** | Threshold 5 attempts → lockout (simulatable) | ✅ Configurable |
| **Password Security** | Plaintext vs bcrypt comparison | ✅ Never stored plaintext; hash verified |

---

## SLIDE 17: CHALLENGES & LEARNINGS

🧗 **Challenges + Solutions**

| Challenge | Solution Applied |
|---|---|
| 🚩 Seat double-booking under concurrent users | Atomic SELECT + UPDATE, Held intermediate state |
| 🚩 Abandoned checkout = seats stuck Held | Frontend countdown + backend can add periodic release job |
| 🚩 3-tier refund logic accuracy | Date subtraction → decision table → display to user BEFORE confirm |
| 🚩 Venue delete wipes events | FK constraint = `RESTRICT` + app-level booking check |
| 🚩 Seat map on mobile screens (375px) | 30px small seats + horizontal scroll acceptable |

### 💡 Key Learnings:
1. **40% of effort = Testing** - 32 TCs took longer to design than to code the features
2. **DB integrity saves you** - FK/CHECK constraints catch bugs app code misses
3. **Edge cases = 80% of complexity** - "Happy path" is 20% work; failures/cancel/refund are 80%
4. **UX > Perfect code** - A seat map users can't understand = useless no matter how correct internally

---

## SLIDE 18: FUTURE ENHANCEMENTS

🚀 **Where the Project Can Go Next**

### P0 - Go-Live Ready:
- PostgreSQL + Alembic migrations (production DB)
- **Real Payment Gateway:** Razorpay / Stripe API integration
- **APScheduler / Celery job** to auto-release expired seat holds
- **Email + SMS** notifications (SMTP + Twilio)

### P1 - Product Features:
- 📱 **QR Check-in** scanner (admin mobile)
- 📋 **Waitlist** for sold-out events → auto-invite on cancel
- 🎟️ **Dynamic pricing** (surge for fast-selling events)
- 🌍 i18n Multi-language + Multi-currency

### P2 - Growth:
- Referral / Affiliate program with commissions
- Customer reviews & ratings system
- Super Admin → Event Manager → Box Office role hierarchy

---

## SLIDE 19: LIVE DEMO WALKTHROUGH

🎬 **Live Demo - 8 Key Screens**

**Step-by-step walkthrough:**
1. 🏠 **Homepage** → Search bar, Category chips, 5 seed event cards
2. 🔍 **Event Detail Page** → Event info, Venue info, 3 Ticket Types
3. 💺 **Seat Selection** → Visual map, select 2 Premium seats, live total
4. 💳 **Checkout Page** → Payment method cards, 10:00 countdown, Pay Rs.3000
5. 🎟️ **Booking Confirmation / E-Ticket** → QR block, seats, print button
6. ❌ **Cancel Test** → Refund estimate pop-up, confirm, seats restored
7. 📊 **Admin Dashboard** → 4 Stat cards, Sales Trend Chart, Top 5 Events bar chart
8. 💸 **Admin → Refunds** → Process refund button → status → Completed

**Demo Credentials:**
- Admin: `admin@ticketbook.com` / `admin123`
- Customer: `rajesh@email.com` / `rajesh123` (or register new)

---

## SLIDE 20: CONCLUSION & Q&A

### ✅ Project Outcome
**17/17 Deliverables Complete | 4/4 Modules Complete | 32/32 Tests Pass**

**Summary of What Was Built:**
🎯 End-to-end **Online Event Ticket Booking System** with professional-grade:
- Requirements analysis (SRS, F/NFR docs)
- UML modeling (Use Case + ER Diagrams in Mermaid)
- Database engineering (BCNF, 9 tables, constraints)
- Full-stack web app (Flask, Jinja2, Bootstrap 5)
- Comprehensive testing (32 TCs, BB/WB/System)
- Documentation (Project Report + Presentation)

**Thank You! Questions & Answers 🙋‍♂️🙋‍♀️**

---
*Presentation Deck Version 1.0 | To deliver as PPT slides with screenshots inserted into each slide body*
