import unittest
from app import app

class TestTesting(unittest.TestCase):
    def test_testing_false(self):
        self.assertFalse(False, "should be false")

    def test_testing_true(self):
        self.assertTrue(True, "should be true")

    def test_testing_fails(self):
        # self.assertTrue(False, "not true")
        self.fail("fail")

class TestTesting2(unittest.TestCase):
    def test_testing_false(self):
        self.assertFalse(False, "should be false")

    def test_test(self):
        self.assertTrue(False, "should be true")

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        print(self.app)
        print(app)
    
    def test_index(self):
        response = self.app.get('/')

        # Check that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    print("All tests have run.")