import unittest
import sys
import os

sys.path.append(os.path.expanduser("~/desktop/flask_app"))

from app import app, db_service
from bson.objectid import ObjectId

class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run before all tests to insert test data"""
        cls.app = app.test_client()
        cls.app.testing = True
        cls.test_drug_id = db_service.db["drugs"].insert_one({
            "name": "Test Drug",
            "company": "Test Company",
            "type": "Prescription",
            "description": "This is a test drug.",
            "stock": 10
        }).inserted_id

    @classmethod
    def tearDownClass(cls):
        """Run after all tests to clean up test data"""
        db_service.db["drugs"].delete_many({"name": {"$regex": "Test Drug"}})
        db_service.db["orders"].delete_many({"name": "Test Order"})

    def test_add_drug(self):
        """Test the functionality of adding a drug"""
        response = self.app.post('/new-drug', data={
            "name": "New Test Drug",
            "company": "Test Company",
            "type": "Prescription",
            "description": "A new test drug.",
            "stock": "5"
        })
        self.assertEqual(response.status_code, 302)  # Confirm redirection is successful
        added_drug = db_service.db["drugs"].find_one({"name": "New Test Drug"})
        self.assertIsNotNone(added_drug)
        db_service.db["drugs"].delete_one({"_id": added_drug["_id"]})  # Clean up data

    def test_add_order(self):
        """Test the functionality of adding an order"""
        # Prepare test order data
        new_order_data = {
            "name": "Test Order",
            "date_of_purchase": "2024-11-25",
            "pickup_or_delivery": "pickup",
            "status": "pending"
        }

        # Send POST request to add the order
        response = self.app.post('/new-order', data=new_order_data)
        self.assertEqual(response.status_code, 302)  # Confirm redirection is successful

        # Verify the order was added to the database
        added_order = db_service.db["orders"].find_one({"name": "Test Order"})
        self.assertIsNotNone(added_order, "Order not found in the database after addition")
        self.assertEqual(added_order["name"], "Test Order")
        self.assertEqual(added_order["pickup_or_delivery"], "pickup")
        self.assertEqual(added_order["status"], "pending")

        # Clean up after test
        db_service.db["orders"].delete_one({"_id": added_order["_id"]})    
    def test_dashboard(self):
        """Test the dashboard data functionality"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        # Adjust to check key elements on the dashboard
        self.assertIn("Drug Inventory", data)

    def test_delete_drug(self):
        """Test the functionality of deleting a drug"""
        response = self.app.post(f'/delete-drug/{self.test_drug_id}', data={"delete": "Yes"})
        self.assertEqual(response.status_code, 302)  # Confirm redirection is successful
        deleted_drug = db_service.db["drugs"].find_one({"_id": self.test_drug_id})
        self.assertIsNone(deleted_drug)
    def test_delete_order(self):
        """Test the functionality of deleting an order"""
        # Step 1: Insert a test order
        test_order = {
            "name": "Order to Delete",
            "date_of_purchase": "2024-11-25",
            "pickup_or_delivery": "delivery",
            "status": "pending"
        }
        inserted_order_id = db_service.db["orders"].insert_one(test_order).inserted_id
        self.assertIsNotNone(inserted_order_id, "Failed to insert test order")
        print(f"Inserted order ID: {inserted_order_id}")

        # Step 2: Send POST request to delete the order
        response = self.app.post(f'/delete-order/{inserted_order_id}', data={"delete": "Yes"})
        self.assertEqual(response.status_code, 302)  # Confirm redirection is successful

        # Step 3: Verify the order was deleted from the database
        deleted_order = db_service.db["orders"].find_one({"_id": inserted_order_id})
        self.assertIsNone(deleted_order, "Order still exists in the database after deletion")

        # Step 4: Clean up in case of unexpected issues
        if deleted_order:
            db_service.db["orders"].delete_one({"_id": inserted_order_id})

if __name__ == '__main__':
    unittest.main()
