import dashboard
import unittest


class TestDashboard(unittest.TestCase):

    def setUp(self):
        dashboard.app.testing = True
        self.app = dashboard.app.test_client()

    def test_home(self):
        result = self.app.get('/')
        # TODO : test assertions 