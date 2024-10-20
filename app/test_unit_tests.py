import unittest

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


if __name__ == "__main__":
    unittest.main()
    print("All tests have run.")