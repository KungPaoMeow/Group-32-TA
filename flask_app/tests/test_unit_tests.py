import unittest
from unittest.mock import patch
from app import app, drugs

# class TestTesting(unittest.TestCase):
#     def test_testing_false(self):
#         self.assertFalse(False, "should be false")

#     def test_testing_true(self):
#         self.assertTrue(True, "should be true")

#     def test_testing_fails(self):
#         # self.assertTrue(False, "not true")
#         self.fail("fail")

# class TestTesting2(unittest.TestCase):
#     def test_testing_false(self):
#         self.assertFalse(False, "should be false")

#     def test_test(self):
#         self.assertTrue(False, "should be true")

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # create new test data to avoid errors with removing from an empty list
        drugs.clear()
        drugs.extend([
            {"name": "drug1", "company": "company1", "type": "Prescription", "stock": 10},
            {"name": "drug2", "company": "company2", "type": "Over-the-Counter", "stock": 5}
        ])
    
    def tearDown(self):
        # reset the list after each test
        drugs.clear()
    
    

    def test_index(self):
        response = self.app.get('/')

        # Check that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_new_drug(self):
        new_drug_test = {"name": "test_name", "company": "test_company", "type": "Prescription", "description": "chymous appetite", "stock": 100}
        response = self.app.post('/new-drug', data=new_drug_test)
        self.assertEqual(response.status_code, 302) # 302 is the redirect status code, new-drug should redirect if info was submitted properly
        self.assertEqual(drugs[-1], new_drug_test)  # check that the last drug in the list is the newly added drug

    def test_delete_drug(self):
        drug = drugs[0]
        response = self.app.post('/delete-drug/0', data=dict(delete="Yes"))
        self.assertEqual(response.status_code, 302)  # check for redirect
        self.assertNotIn(drug, drugs)

    def test_edit_drug(self):
        drug_old = drugs[0].copy()
        drug_new = {"name": "test_name", "company": "test_company", "type": "Prescription", "description": "chymous appetite", "stock": drug_old["stock"] + 1}
        response = self.app.post('/drug-edit/0', data=drug_new)
        self.assertEqual(response.status_code, 302) # check for redirect
        self.assertNotIn(drug_old, drugs)
        self.assertEqual(drug_new, drugs[0])
        

if __name__ == "__main__":
    unittest.main()
    print("All tests have run.")