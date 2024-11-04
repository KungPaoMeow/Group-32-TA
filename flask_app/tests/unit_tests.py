from datetime import date
import unittest
from unittest.mock import patch
from bson.objectid import ObjectId
from app import app, db

drugs = []
orders = []
drug_inv_collection = db["drugs"]
order_collection = db["orders"]

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


    # drug tests
    def test_new_and_edit_and_delete_drug(self):
        new_drug_data = {"name": "test_name", "company": "test_company", "type": "Prescription", "description": "chymous appetite", "stock": 100}
        
        # New drug test
        response = self.app.post("/new-drug", data = new_drug_data)
        new_drug = drug_inv_collection.find_one(new_drug_data)
        self.assertIsNotNone(new_drug, "Test data did not make it to the database")
        self.assertEqual(response.status_code, 302) # 302 is the redirect status code, new-drug should redirect if info was submitted properly

        # Edit that new drug test
        edited_drug_data = new_drug_data
        edited_drug_data["name"] = "edited_name"
        response = self.app.post(f"/drug-edit/{new_drug['_id']}", data = edited_drug_data)
        edited_drug = drug_inv_collection.find_one(edited_drug_data)
        self.assertNotEqual(new_drug, edited_drug)
        self.assertEqual(response.status_code, 302)

        # Delete that new drug test
        response = self.app.post(f"/delete-drug/{edited_drug['_id']}", data = {"delete": "Yes"})
        should_be_none = drug_inv_collection.find_one(edited_drug)
        self.assertIsNone(should_be_none)
        self.assertEqual(response.status_code, 302)

    def test_drug_search(self):
        test_collection_name = "temp"
        test_collection = db[test_collection_name]
        test_data = [
            {"name": "drug1", "company": "company1", "type": "Prescription", "stock": 10},
            {"name": "drug2", "company": "company1", "type": "Prescription", "stock": 10},
            {"name": "awDRUh21", "company": "company1", "type": "Prescription", "stock": 10},
            {"name": "loremipsum", "company": "company1", "type": "Prescription", "stock": 10}
        ]

        test_collection.insert_many(test_data)  # Add test data to DB
        filters = ["", "dru", "chyme"]
        shouldBeFilteredTo = [["drug1", "drug2", "awdruh21", "loremipsum"], ["drug1", "drug2", "awdruh21"], []]

        try:
            for filter in filters:
                response = self.app.get(f"/drug-search?q={filter}&test={test_collection_name}")
                self.assertEqual(response.status_code, 200, "HTTP GET request to route /drug-search should return OK")

                # Get list of drugs being displayed on site
                filteredDrugs = response.get_json()
                answer = shouldBeFilteredTo[filters.index(filter)]
                self.assertEqual(set(filteredDrugs), set(answer), "Drugs are not being filtered properly")
        finally:
            test_collection.drop()


    # order tests
    def test_new_and_edit_and_delete_order(self):
        new_order_test = {"name": "test_name", "date_of_purchase": "2024-01-15", "pickup_or_delivery": "Delivery", "status": "Delivered"}

        # New drug test
        response = self.app.post("/new-order", data = new_order_test)
        new_order = order_collection.find_one(new_order_test)
        self.assertIsNotNone(new_order, "Test data did not make it to the database")
        self.assertEqual(response.status_code, 302) # 302 is the redirect status code, new-drug should redirect if info was submitted properly

        # Edit that new drug test
        edited_order_data = new_order_test
        edited_order_data["name"] = "edited_name"
        response = self.app.post(f"/edit-order/{new_order['_id']}", data = edited_order_data)
        edited_order = order_collection.find_one(edited_order_data)
        self.assertNotEqual(new_order, edited_order)
        self.assertEqual(response.status_code, 302)

        # Delete that new drug test
        response = self.app.post(f"/delete-order/{edited_order['_id']}", data = {"delete": "Yes"})
        should_be_none = order_collection.find_one(edited_order)
        self.assertIsNone(should_be_none)
        self.assertEqual(response.status_code, 302)

    def test_new_drug_invalid_stock(self):
        invalid_drug = {"name": "Invalid Drug", "company": "Invalid Co", "type": "Prescription", "stock": "invalid_stock"}
        response = self.app.post("/new-drug", data=invalid_drug)
        self.assertEqual(response.status_code, 400)

    def test_new_order_invalid_date(self):
        invalid_order = {"name": "Test Order", "date_of_purchase": "invalid_date", "pickup_or_delivery": "Delivery", "status": "Delivered"}
        response = self.app.post("/new-order", data=invalid_order)
        self.assertEqual(response.status_code, 400)



if __name__ == "__main__":
    unittest.main()
    print("All tests have run.")
