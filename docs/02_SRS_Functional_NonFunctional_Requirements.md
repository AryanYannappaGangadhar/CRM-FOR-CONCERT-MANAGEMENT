# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Online Event Ticket Booking System

**Document Version:** 1.0  
**Date:** August 2026  
**Prepared For:** Software Engineering Project Submission

---

## TABLE OF CONTENTS
1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [System Architecture](#5-system-architecture)
6. [User Characteristics](#6-user-characteristics)
7. [Interface Requirements](#7-interface-requirements)

---

## 1. INTRODUCTION

### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a comprehensive description of the requirements for the Online Event Ticket Booking System. It includes functional, non-functional, and interface requirements that serve as guidelines for developers, testers, and stakeholders throughout the project lifecycle.

### 1.2 Intended Audience
- Project Developers
- Software Testers
- Project Managers
- Event Organizers (Clients)
- Academic Evaluators

### 1.3 Definitions, Acronyms, and Abbreviations
| Term | Definition |
|------|------------|
| SRS | Software Requirements Specification |
| CRUD | Create, Read, Update, Delete |
| PK | Primary Key |
| FK | Foreign Key |
| UI | User Interface |
| UX | User Experience |
| API | Application Programming Interface |
| DB | Database |
| 2FA | Two-Factor Authentication |
| OTP | One-Time Password |
| QR Code | Quick Response Code |
| UPI | Unified Payments Interface |

### 1.4 References
- IEEE Recommended Practice for Software Requirements Specifications (IEEE 830-1998)
- Project Allocation Document with Module Definitions
- Software Engineering Course Syllabus

---

## 2. OVERALL DESCRIPTION

### 2.1 Product Perspective
The Online Event Ticket Booking System is a self-contained, web-based application that serves as a centralized platform for event ticketing. It interfaces with:
- **Frontend:** Responsive web UI accessible via standard browsers
- **Backend:** Flask-based Python server with business logic
- **Database:** SQLite relational database with proper normalization
- **External Systems:** Payment Gateway (simulated), Email Service (simulated)

### 2.2 Product Functions Summary
| Module | Key Functions |
|--------|---------------|
| Event & Venue Management | Event CRUD, Venue CRUD, Event-Venue mapping, Event categorization |
| Customer & Ticket Management | User registration, Login/Logout, Profile management, Ticket types, E-tickets |
| Seat & Booking Management | Seat map, Seat selection, Booking CRUD, Temporary holding, Booking history |
| Payment, Cancellation & Refund | Payment processing, Cancellation requests, Refund calculation, Status tracking |

### 2.3 Operating Environment
- **Operating System:** Cross-platform (Windows, Linux, macOS)
- **Web Server:** Flask Development Server (Production: Gunicorn/Nginx)
- **Database:** SQLite 3.x
- **Browser Support:** Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Screen Resolution:** 1366x768 and above (Responsive design supports lower)

---

## 3. FUNCTIONAL REQUIREMENTS

### FR-001: USER AUTHENTICATION MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001.1 | System shall allow new users to register with name, email, phone, and password | High |
| FR-001.2 | System shall validate that email addresses are unique and in correct format | High |
| FR-001.3 | System shall encrypt passwords using secure hashing (e.g., bcrypt) before storage | High |
| FR-001.4 | System shall allow registered users to login using email and password | High |
| FR-001.5 | System shall display error message for incorrect login credentials | High |
| FR-001.6 | System shall implement session timeout after 30 minutes of inactivity | Medium |
| FR-001.7 | System shall provide separate login for Admin users | High |
| FR-001.8 | System shall allow users to update their profile information | Medium |

### FR-002: EVENT MANAGEMENT MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-002.1 | Admin shall be able to create new events with name, date, time, description, and category | High |
| FR-002.2 | System shall allow event image/banner upload (JPEG, PNG, max 5MB) | Medium |
| FR-002.3 | Admin shall be able to view, edit, and delete existing events | High |
| FR-002.4 | System shall support event categories: Concert, Conference, Sports, Theater, Workshop, Other | Medium |
| FR-002.5 | System shall display published events to customers on the homepage | High |
| FR-002.6 | Admin shall be able to change event status: Draft, Published, Sold Out, Completed, Cancelled | High |
| FR-002.7 | System shall allow customers to search and filter events by category, date, and keyword | Medium |
| FR-002.8 | System shall display event details page with all relevant information | High |

### FR-003: VENUE MANAGEMENT MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-003.1 | Admin shall be able to create venues with name, address, capacity, and amenities | High |
| FR-003.2 | System shall generate a seat map based on venue capacity and layout | Medium |
| FR-003.3 | Admin shall be able to view, edit, and delete venues (with dependency checks) | High |
| FR-003.4 | System shall allow one venue to be associated with multiple events | High |
| FR-003.5 | System shall prevent deletion of a venue if events are scheduled there | Medium |
| FR-003.6 | System shall display venue details (address, amenities, capacity) on event pages | Medium |

### FR-004: TICKET MANAGEMENT MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-004.1 | Admin shall be able to define multiple ticket types per event (VIP, Premium, Standard, etc.) | High |
| FR-004.2 | Each ticket type shall have configurable price, quantity, and benefits description | High |
| FR-004.3 | System shall track remaining ticket count per type in real-time | High |
| FR-004.4 | System shall generate unique e-tickets with booking ID, QR/barcode data upon confirmation | High |
| FR-004.5 | Customers shall be able to view and download their e-tickets as PDF/Printable format | Medium |
| FR-004.6 | System shall display booking history for each customer | High |
| FR-004.7 | Admin shall be able to view all tickets sold for any event | High |

### FR-005: SEAT MANAGEMENT MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-005.1 | System shall display an interactive visual seat map for selected event | High |
| FR-005.2 | Seat map shall differentiate Available, Selected, Booked, and Reserved seats with colors | High |
| FR-005.3 | System shall implement real-time seat availability with concurrency control | High |
| FR-005.4 | Selected seats shall be temporarily held for 10 minutes during checkout | Medium |
| FR-005.5 | System shall release held seats automatically if payment not completed within time | Medium |
| FR-005.6 | Each seat shall be uniquely identifiable (Row + Seat Number) | High |
| FR-005.7 | System shall prevent double booking of the same seat | High |
| FR-005.8 | Customers shall be able to select up to 10 seats per transaction | Medium |

### FR-006: BOOKING MANAGEMENT MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-006.1 | System shall generate a unique Booking ID for each successful transaction | High |
| FR-006.2 | Booking shall capture: Customer ID, Event ID, Seats, Ticket Type, Total Amount, Date/Time | High |
| FR-006.3 | System shall calculate total booking amount dynamically based on seats and ticket prices | High |
| FR-006.4 | Customers shall receive booking confirmation via email and in-app notification | Medium |
| FR-006.5 | Customers shall be able to view all their past and upcoming bookings | High |
| FR-006.6 | Admin shall be able to view all bookings, filter by event/customer/date | High |
| FR-006.7 | System shall restrict booking modifications within 24 hours of event time | Medium |
| FR-006.8 | System shall support waitlist for sold-out events (optional) | Low |

### FR-007: PAYMENT MANAGEMENT MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-007.1 | System shall support multiple payment methods: Credit/Debit Card, UPI, Net Banking, Wallet | High |
| FR-007.2 | System shall validate card details (number format, expiry, CVV) before processing | High |
| FR-007.3 | System shall display transaction summary before final payment confirmation | High |
| FR-007.4 | Each successful payment shall generate a unique Transaction ID | High |
| FR-007.5 | System shall log all payment attempts (success, failed, pending) for audit | High |
| FR-007.6 | System shall provide payment retry option for failed transactions | Medium |
| FR-007.7 | System shall generate payment receipt in downloadable format | Medium |
| FR-007.8 | All payment data shall be transmitted over secure HTTPS connection | High |

### FR-008: CANCELLATION & REFUND MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-008.1 | Customers shall be able to request cancellation of confirmed bookings | High |
| FR-008.2 | System shall display cancellation policy and refund amount before confirmation | High |
| FR-008.3 | Cancellation policy: 100% refund if >7 days before event, 50% if 3-7 days, 0% if <3 days | High |
| FR-008.4 | System shall calculate refund amount automatically based on cancellation date | High |
| FR-008.5 | Cancelled seats shall be released back to available inventory immediately | High |
| FR-008.6 | Refund status shall be tracked: Initiated → Processing → Completed → Failed | High |
| FR-008.7 | Customers shall be able to view refund status for cancelled bookings | Medium |
| FR-008.8 | Admin shall be able to override and process manual refunds if needed | Medium |
| FR-008.9 | System shall send cancellation and refund status notifications | Medium |

### FR-009: ADMIN DASHBOARD MODULE
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-009.1 | Admin dashboard shall display key metrics: Total Events, Total Bookings, Total Revenue | High |
| FR-009.2 | Dashboard shall show graphical charts for sales trends and event performance | Medium |
| FR-009.3 | Admin shall be able to manage all user accounts (view, activate/deactivate) | Medium |
| FR-009.4 | System shall allow admin to generate reports (Event-wise sales, Daily revenue, Customer list) | Medium |
| FR-009.5 | Admin shall be able to mark attendance/check-in for ticket holders at event | Low |

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### NFR-01: PERFORMANCE REQUIREMENTS
| ID | Requirement | Target Value |
|----|-------------|--------------|
| NFR-01.1 | Page Load Time | ≤ 3 seconds on 4G connection |
| NFR-01.2 | Login Response Time | ≤ 2 seconds |
| NFR-01.3 | Seat Availability Check | ≤ 1 second |
| NFR-01.4 | Booking Completion Time | ≤ 5 seconds (excluding payment gateway) |
| NFR-01.5 | Concurrent Users | System shall support ≥ 500 concurrent users |
| NFR-01.6 | Database Query Response | ≤ 500ms for standard queries |
| NFR-01.7 | System Throughput | ≥ 100 bookings per minute |

### NFR-02: SECURITY REQUIREMENTS
| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-02.1 | Password Storage | bcrypt hashing with salt rounds ≥ 12 |
| NFR-02.2 | Data Transmission | All communication via HTTPS/TLS 1.2+ |
| NFR-02.3 | Authentication | Session-based with secure HTTPOnly cookies |
| NFR-02.4 | SQL Injection Protection | Use parameterized queries / ORM |
| NFR-02.5 | XSS Protection | Input validation, output encoding |
| NFR-02.6 | CSRF Protection | CSRF tokens for all state-changing forms |
| NFR-02.7 | Role-Based Access | Admin vs Customer role separation enforced |
| NFR-02.8 | Payment Card Data | No storage of full card numbers (tokenization) |
| NFR-02.9 | Data Privacy | Customer PII accessible only to authorized admins |
| NFR-02.10 | Failed Login Attempts | Account lockout after 5 consecutive failures |

### NFR-03: AVAILABILITY & RELIABILITY
| ID | Requirement | Target |
|----|-------------|--------|
| NFR-03.1 | System Availability | 99.9% uptime (excluding scheduled maintenance) |
| NFR-03.2 | Mean Time Between Failures | ≥ 100 hours |
| NFR-03.3 | Mean Time To Recover | ≤ 30 minutes |
| NFR-03.4 | Data Backup | Daily automated database backups |
| NFR-03.5 | Transaction Integrity | ACID compliance for all booking/payment transactions |

### NFR-04: USABILITY REQUIREMENTS
| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-04.1 | User Training | Customer features shall be usable without formal training |
| NFR-04.2 | Error Messages | Plain language, non-technical error messages for users |
| NFR-04.3 | Navigation | Maximum 3 clicks to reach any feature from homepage |
| NFR-04.4 | Help System | Tooltips and inline help where needed |
| NFR-04.5 | Accessibility | WCAG 2.1 Level AA compliance (contrast, screen reader support) |
| NFR-04.6 | Language | English (initial release) |

### NFR-05: COMPATIBILITY REQUIREMENTS
| ID | Requirement | Details |
|----|-------------|---------|
| NFR-05.1 | Browser Compatibility | Chrome 90+, Firefox 88+, Edge 90+, Safari 14+ |
| NFR-05.2 | Mobile Responsive | Bootstrap grid, works on 320px (mobile) to 2560px (4K) |
| NFR-05.3 | OS Compatibility | Windows 10+, macOS 11+, Linux (Ubuntu 20.04+) |
| NFR-05.4 | Device Support | Desktop, Laptop, Tablet, Smartphone |

### NFR-06: SCALABILITY REQUIREMENTS
| ID | Requirement | Details |
|----|-------------|---------|
| NFR-06.1 | Database Scalability | Shall support 100,000+ records in all major tables |
| NFR-06.2 | Horizontal Scaling | Application layer shall be stateless for load balancing |
| NFR-06.3 | File Storage | Shall handle 10,000+ event image uploads |

### NFR-07: MAINTAINABILITY
| ID | Requirement | Details |
|----|-------------|---------|
| NFR-07.1 | Code Comments | Inline documentation for all complex logic |
| NFR-07.2 | Modular Design | Separate modules for Event, Customer, Booking, Payment |
| NFR-07.3 | Version Control | Git-based source code management |
| NFR-07.4 | Configuration | Environment variables for DB credentials, API keys |

---

## 5. SYSTEM ARCHITECTURE

### 5.1 Architectural Pattern: 3-Tier Client-Server Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                      │
│  (HTML5, CSS3, Bootstrap 5, JavaScript, Responsive UI)       │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTPS / REST APIs
┌──────────────────────────────▼───────────────────────────────┐
│                      APPLICATION LAYER                       │
│  (Flask / Python, Business Logic, Controllers, Services)     │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                        DATA ACCESS LAYER                     │
│              (SQLite DB, SQLAlchemy ORM, Queries)            │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Technology Stack
| Component | Technology |
|-----------|------------|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript (ES6+), Chart.js |
| Backend | Python 3.9+, Flask Framework 2.3+ |
| Database | SQLite 3.x (Development), PostgreSQL (Production ready) |
| ORM | SQLAlchemy 2.x |
| Password Security | Werkzeug Security (bcrypt) |
| Session Management | Flask-Session (Server-side sessions) |
| Input Validation | Flask-WTF, WTForms |
| PDF Generation | ReportLab / WeasyPrint (for e-tickets) |
| Charting | Chart.js (for admin dashboard) |

---

## 6. USER CHARACTERISTICS

### 6.1 User Roles

| Role | Description | Technical Proficiency |
|------|-------------|----------------------|
| **Customer** | End users who browse events, book tickets, manage bookings | Basic computer knowledge |
| **Event Organizer (Admin)** | Manages events, venues, bookings, refunds | Moderate technical skills |
| **Super Admin** | Full system access, user management, reports | Technical background preferred |

### 6.2 User Personas

**Persona 1: Customer**
- Age: 18-60 years
- Education: High School+
- Goals: Find events, book tickets quickly, manage bookings
- Pain Points: Complex UIs, hidden charges, unclear refund policies

**Persona 2: Admin**
- Role: Event Manager / Box Office Operator
- Education: College Graduate
- Goals: Create events quickly, track sales, manage cancellations
- Pain Points: Slow admin panels, lack of reporting

---

## 7. INTERFACE REQUIREMENTS

### 7.1 User Interfaces (UI)
- **Home Page:** Search bar, Event categories, Featured events carousel
- **Event List Page:** Filterable grid of events with date, venue, price
- **Event Detail Page:** Event info, ticket types, seat selection button
- **Seat Selection Page:** Interactive seat map, running total, checkout button
- **Checkout Page:** Customer info, payment method selection, order summary
- **Customer Dashboard:** Profile, Booking history, Download tickets, Cancel booking
- **Admin Dashboard:** Stats cards, charts, quick links to all modules
- **Admin Forms:** Event form, Venue form, Ticket type forms

### 7.2 Hardware Interfaces
None specific - standard web server and client hardware

### 7.3 Software Interfaces
- **Payment Gateway API:** Simulated (integration-ready for Razorpay/Stripe)
- **Email Service:** SMTP (simulated for development)
- **Database API:** SQLAlchemy ORM → SQLite

### 7.4 Communication Interfaces
- Protocol: HTTPS (TLS 1.2+)
- Data Format: JSON for API responses
- Authentication: Session cookies (HTTPOnly, Secure flag)

---

*Document Version: 1.0 | Status: Final*
