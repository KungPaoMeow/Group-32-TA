from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os


class MongoDB:
    def __init__(self) -> None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except:
            pass

        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        uri = os.getenv('DB_CONN_STRING')

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            self.client = None
            print(e)
            return

        self.client = client

        # Get or create db collection if does not exist
        db = self.client['pharmacy_db']
        self.db = db