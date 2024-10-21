from datetime import date
import unittest
from unittest.mock import patch
from app import app, drugs, orders

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

        orders.clear()
        orders.extend([
            {"name": "name1", "date_of_purchase": date(2024, 10, 20), "pickup_or_delivery": "Delivery", "status": "Delivered"},
            {"name": "name2", "date_of_purchase": date(2024, 10, 21), "pickup_or_delivery": "Pick up", "status": "Awaiting Pickup"}
        ])
    
    # def tearDown(self):
    #     # reset the list after each test
    #     drugs.clear()

    # def test_index(self):
    #     response = self.app.get('/')

    #     # Check that the status code is 200 OK
    #     self.assertEqual(response.status_code, 200)

    # drug tests
    def test_new_drug(self):
        new_drug_test = {"name": "test_name", "company": "test_company", "type": "Prescription", "description": "chymous appetite", "stock": 100}
        response = self.app.post("/new-drug", data = new_drug_test)
        self.assertEqual(response.status_code, 302) # 302 is the redirect status code, new-drug should redirect if info was submitted properly
        self.assertEqual(drugs[-1], new_drug_test)  # check that the last drug in the list is the newly added drug

    def test_delete_drug(self):
        drug = drugs[0]
        response = self.app.post("/delete-drug/0", data = {"delete": "Yes"})
        self.assertEqual(response.status_code, 302)  # check for redirect
        self.assertNotIn(drug, drugs)

    def test_edit_drug(self):
        drug_old = drugs[0].copy()
        drug_new = {"name": "test_name", "company": "test_company", "type": "Prescription", "description": "chymous appetite", "stock": drug_old["stock"] + 1}
        response = self.app.post("/drug-edit/0", data = drug_new)
        self.assertEqual(response.status_code, 302) # check for redirect
        self.assertNotIn(drug_old, drugs)
        self.assertEqual(drug_new, drugs[0])

    def test_drug_search(self):
        drugs.extend([
            {"name": "awDRUh21", "company": "company1", "type": "Prescription", "stock": 10},
            {"name": "loremipsum", "company": "company1", "type": "Prescription", "stock": 10}
        ])
        filters = ["", "dru", "chyme"]
        shouldBeFilteredTo = [["drug1", "drug2", "awdruh21", "loremipsum"], ["drug1", "drug2", "awdruh21"], []]
        for filter in filters:
            response = self.app.get(f"/drug-search?q={filter}")
            self.assertEqual(response.status_code, 200, "HTTP GET request to route /drug-search should return OK")

            # Get list of drugs being displayed on site
            filteredDrugs = response.get_json()
            answer = shouldBeFilteredTo[filters.index(filter)]
            self.assertEqual(set(filteredDrugs), set(answer), "Drugs are not being filtered properly")


    # order tests
    def test_new_order(self):
        new_order_test = {"name": "test_name", "date_of_purchase": date(2024, 10, 20), "pickup_or_delivery": "Delivery", "status": "Delivered"}
        response = self.app.post("/new-order", data = new_order_test)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(orders[-1], new_order_test)

    def test_delete_order(self):
        order = orders[0]
        response = self.app.post("/delete-order/0", data = {"delete": "Yes"})
        self.assertEqual(response.status_code, 302) #ensure redirect
        self.assertNotIn(order, orders)
    
    def test_edit_order(self):
        order_old = orders[0].copy()
        order_new = {"name": "test_name", "date_of_purchase": date(2024, 12, 20), "pickup_or_delivery": "Pick up", "status": "Picked Up"}
        response = self.app.post("/edit-order/0", data = order_new)
        self.assertEqual(response.status_code, 302) # check for redirect
        self.assertNotIn(order_old, orders)
        self.assertEqual(order_new, orders[0])


if __name__ == "__main__":
    unittest.main()
    print("All tests have run.")