"""
Online Event Ticket Booking System - Automated Smoke Tests
Runs 16+ integration tests against the running Flask server.
Usage: python -m pytest tests/smoke_test.py -v  OR  python tests/smoke_test.py
"""

import urllib.request, urllib.parse, http.cookiejar, sys, unittest

BASE = 'http://127.0.0.1:5000'

def make_opener():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

class SmokeTest(unittest.TestCase):
    def setUp(self):
        self.opener = make_opener()

    def request(self, path, data=None, method='GET', expected=200):
        url = f'{BASE}{path}'
        try:
            if data:
                req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method=method)
            else:
                req = urllib.request.Request(url, method=method)
            resp = self.opener.open(req, timeout=15)
            self.assertEqual(resp.status, expected, f'HTTP {resp.status} vs {expected}')
            return resp.read().decode()
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, expected, f'HTTP {e.code} vs {expected}')
            return e.read().decode() if hasattr(e, 'read') else ''

    # --- Module: Home & Public ---
    def test_01_homepage(self):
        html = self.request('/')
        self.assertIn('EventBook Pro', html)
        self.assertIn('Summer Music Festival', html)

    def test_02_login_page(self):
        html = self.request('/login')
        self.assertIn('Login', html)

    def test_03_register_page(self):
        html = self.request('/register')
        self.assertIn('Create Account', html)

    def test_04_event_detail(self):
        html = self.request('/event/1')
        self.assertIn('Summer Music Festival', html)
        self.assertIn('Grand Arena', html)

    # --- Module: Auth & Admin ---
    def test_05_admin_login(self):
        html = self.request('/login', data={
            'email': 'admin@ticketbook.com', 'password': 'admin123'
        }, method='POST')
        self.assertNotIn('Invalid email', html)

    def test_06_admin_dashboard(self):
        self.test_05_admin_login()
        html = self.request('/admin/dashboard')
        self.assertIn('Dashboard', html)
        self.assertIn('Total Events', html)

    def test_07_admin_events(self):
        self.test_05_admin_login()
        html = self.request('/admin/events')
        self.assertIn('Tech Summit', html)

    def test_08_admin_venues(self):
        self.test_05_admin_login()
        html = self.request('/admin/venues')
        self.assertIn('Grand Arena', html)

    def test_09_admin_customers(self):
        self.test_05_admin_login()
        html = self.request('/admin/customers')
        self.assertIn('Rajesh', html)

    def test_10_admin_refunds(self):
        self.test_05_admin_login()
        html = self.request('/admin/refunds')
        self.assertIn('Refund', html)

    # --- Module: Seat & Booking (Customer) ---
    def login_customer(self):
        return self.request('/login', data={
            'email': 'rajesh@email.com', 'password': 'rajesh123'
        }, method='POST')

    def test_11_customer_login(self):
        html = self.login_customer()
        self.assertNotIn('Invalid email', html)

    def test_12_seat_selection(self):
        self.login_customer()
        html = self.request('/event/1/seats')
        self.assertIn('STAGE', html)
        self.assertIn('seat-row', html.lower())

    def test_13_profile_page(self):
        self.login_customer()
        html = self.request('/profile')
        self.assertIn('Rajesh', html)
        self.assertIn('Booking Summary', html)

    def test_14_my_bookings(self):
        self.login_customer()
        html = self.request('/bookings')
        self.assertIn('My Bookings', html)

    # --- Module: API & Misc ---
    def test_15_seat_json_api(self):
        import json
        html = self.request('/api/seats/1')
        data = json.loads(html)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 100)  # Venue has 2000 capacity

    def test_16_404_handler(self):
        html = self.request('/thispagedefinitelydoesnotexistxyz123', expected=404)
        self.assertTrue(True)  # HTTP status checked by request()


if __name__ == '__main__':
    print(f'Running tests against: {BASE}')
    print('Make sure the Flask server is running!\n')
    suite = unittest.TestLoader().loadTestsFromTestCase(SmokeTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
