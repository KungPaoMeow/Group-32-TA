from datetime import date
import unittest
from unittest.mock import patch,MagicMock
from bson.objectid import ObjectId
from app import app, db
from pymongo.errors import ConnectionFailure
from pymongo_get_db import MongoDB

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

    # Test editing a non-existent order
    def test_edit_order_not_found(self):
        fake_id = "000000000000000000000000"
        response = self.app.post(f'/edit-order/{fake_id}', data={"name": "test"})
        self.assertEqual(response.status_code, 404)

    # Test deleting a non-existent order
    def test_delete_order_not_found(self):
        fake_id = "000000000000000000000000"
        response = self.app.post(f'/delete-order/{fake_id}', data={"delete": "Yes"})
        self.assertEqual(response.status_code, 404)
    # Test the drug information page
    def test_drug_info(self):
        response = self.app.get('/drug-info')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Drug Information', response.data)

    # Test deleting a non-existent drug
    def test_delete_drug_not_found(self):
        fake_id = "000000000000000000000000"
        response = self.app.post(f'/delete-drug/{fake_id}', data={"delete": "Yes"})
        self.assertEqual(response.status_code, 404)

    # Test POST request for the index page (index page was removed, but can still test that POST requests fail on dashboard)
    def test_index_post_should_fail(self):
        response = self.app.post('/', data={'user_input': 'test input'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You entered: test input', response.data)

    # Test the dashboard page
    def test_dashboard(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    # Test adding a sample drug
    def test_add_sample_drug(self):
        response = self.app.get('/add-sample-drug')
        data = response.get_json()
        self.assertIn(response.status_code, [201, 409])
        if response.status_code == 201:
            self.assertIn("Drug added successfully", data["msg"])
        else:
            self.assertIn("Drug already exists in the database.", data["msg"])

    # Test the order tracking page
    def test_order_tracking(self):
        response = self.app.get('/order-tracking')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Order Data', response.data)
        
    def test_drug_edit(self):
        # First, add a sample drug to edit
        new_drug_data = {"name": "test_drug", "company": "test_company", "type": "Prescription", "description": "test drug description", "stock": 100}
        inserted_id = drug_inv_collection.insert_one(new_drug_data).inserted_id

        # Now edit the drug
        edited_drug_data = {
            "name": "edited_drug",
            "company": "edited_company",
            "type": "Over-the-Counter",
            "description": "edited description",
            "stock": 50
        }
        response = self.app.post(f'/drug-edit/{inserted_id}', data=edited_drug_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after editing

        # Verify changes in the database
        edited_drug = drug_inv_collection.find_one({"_id": inserted_id})
        self.assertEqual(edited_drug["name"], "edited_drug")
        self.assertEqual(edited_drug["company"], "edited_company")
        self.assertEqual(edited_drug["type"], "Over-the-Counter")
        self.assertEqual(edited_drug["description"], "edited description")
        self.assertEqual(edited_drug["stock"], 50)

        # Clean up by deleting the test drug
        drug_inv_collection.delete_one({"_id": inserted_id})
        
    def test_drug_edit_invalid_stock(self):
        # First, add a sample drug to edit
        new_drug_data = {"name": "test_drug", "company": "test_company", "type": "Prescription", "description": "test drug description", "stock": 100}
        inserted_id = drug_inv_collection.insert_one(new_drug_data).inserted_id

        # Try to edit the drug with an invalid stock value
        edited_drug_data = {
            "name": "edited_drug",
            "company": "edited_company",
            "type": "Over-the-Counter",
            "description": "edited description",
            "stock": "invalid_stock"  # Invalid stock value
        }
        response = self.app.post(f'/drug-edit/{inserted_id}', data=edited_drug_data)
        self.assertEqual(response.status_code, 400)  # Expecting a 400 error for invalid input

        # Clean up by deleting the test drug
        drug_inv_collection.delete_one({"_id": inserted_id})

    # Test drug creation page with redirect
    def test_new_drug_with_redirect(self):
        new_drug_data = {
            "name": "redirect_drug",
            "company": "redirect_company",
            "type": "Prescription",
            "description": "redirect description",
            "stock": 10
        }
        response = self.app.post('/new-drug', data=new_drug_data, query_string={'from': 'info'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to /drug-info

        # Verify that the drug was added to the database
        inserted_drug = drug_inv_collection.find_one({"name": "redirect_drug"})
        self.assertIsNotNone(inserted_drug)

        # Clean up by deleting the test drug
        drug_inv_collection.delete_one({"_id": inserted_drug["_id"]})

    # Test the inventory monitoring page
    def test_inv_monitoring(self):
        response = self.app.get('/inv-monitoring')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Monitor Inventory', response.data)

    # Test new order creation with redirect
    def test_new_order_with_redirect(self):
        """Test creating a new order with a redirect back to order tracking"""
        new_order_data = {
            "name": "redirect_order",
            "date_of_purchase": "2024-01-01",
            "pickup_or_delivery": "pickup",
            "status": "pending"
        }
        response = self.app.post('/new-order', data=new_order_data, query_string={'from': 'order-tracking'})
        self.assertEqual(response.status_code, 302)  # Expecting redirect to /order-tracking

        # Verify the order was added to the database
        inserted_order = order_collection.find_one({"name": "redirect_order"})
        self.assertIsNotNone(inserted_order)

        # Clean up by deleting the test order
        order_collection.delete_one({"_id": inserted_order["_id"]})

    # Test delete confirmation page for order
    def test_delete_order_confirmation(self):
        """Test loading delete confirmation page for an order"""
        # First, add a sample order to delete
        new_order_data = {
            "name": "test_order",
            "date_of_purchase": "2024-01-01",
            "pickup_or_delivery": "pickup",
            "status": "pending"
        }
        inserted_id = order_collection.insert_one(new_order_data).inserted_id

        # Access delete confirmation page
        response = self.app.get(f'/delete-order/{inserted_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Delete Order', response.data)

        # Clean up by deleting the test order
        order_collection.delete_one({"_id": inserted_id})

    # Test accessing drug edit page with a non-existent ID
    def test_drug_edit_non_existent_id(self):
        """Test editing a drug that does not exist"""
        fake_id = "000000000000000000000000"
        response = self.app.get(f'/drug-edit/{fake_id}')
        self.assertEqual(response.status_code, 404)

    # Test accessing delete drug confirmation page with a non-existent ID
    def test_delete_drug_page_non_existent_id(self):
        """Test accessing delete page for a non-existent drug"""
        fake_id = "000000000000000000000000"
        response = self.app.get(f'/delete-drug/{fake_id}')
        self.assertEqual(response.status_code, 404)     

    # Test browsing drugs page
    def test_browse_drug_page(self):
        """Test loading the browse drug page"""
        response = self.app.get('/browse-drug')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Browse Drugs', response.data)

    # Test searching for drugs with a specific query
    def test_drug_search_with_query(self):
        """Test searching for drugs with a specific query"""
        # Insert a sample drug for testing search
        drug_data = {"name": "search_test_drug", "company": "test_company", "type": "Prescription", "description": "test description", "stock": 20}
        drug_inv_collection.insert_one(drug_data)

        # Perform search
        response = self.app.get('/drug-search?q=search_test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'search_test_drug', response.data)

        # Clean up by deleting the test drug
        drug_inv_collection.delete_one({"name": "search_test_drug"})

    # Test loading add sample order page
    def test_add_sample_order(self):
        """Test loading the add sample order page"""
        response = self.app.get('/add-sample-order')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sample order added', response.data)

        
    @patch('pymongo_get_db.MongoClient')
    @patch('builtins.print')  # Patch print to capture print output
    def test_ping_failure(self, mock_print, MockMongoClient):
        """Test exception handling during MongoDB ping"""
        # Create a mock client with `command` method raising ConnectionFailure
        mock_client = MagicMock()
        mock_client.admin.command.side_effect = ConnectionFailure("Ping failed")
        MockMongoClient.return_value = mock_client
        
        # Run MongoDB to trigger the exception in the ping
        MongoDB()
        
        # Check if the error message is printed
        mock_print.assert_called()  # Ensure print was called
        printed_output = mock_print.call_args[0][0]
        self.assertIn("Ping failed", str(printed_output))  # Check output contains "Ping failed"



if __name__ == "__main__":
    unittest.main()
    print("All tests have run.")
