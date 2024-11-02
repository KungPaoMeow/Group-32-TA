from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


class MongoDB:
    def __init__(self) -> None:
        load_dotenv()
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        uri = os.getenv('DB_CONN_STRING')

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.client = client

        # Get or create db collection if does not exist
        db = self.client['pharmacy_db']
        self.db = db

    # def test_db(self):
    #     # Add mock data - dictionary
    #     dashboard = {
    #         'total_orders' : 888,
    #         'drug_inventory' : 123974,
    #         'earnings' : 123114,
    #         'order_increase' : 201,
    #         'inventory_increase' : 2100,
    #         'earnings_increase' : 11981
    #     }
    #     # Return the collection
    #     return db
        