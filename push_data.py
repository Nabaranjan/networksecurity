import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import os
import sys
import json
import pymongo
import pandas as pd
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            db = self.mongo_client[database]  # Get the database
            col = db[collection]  # Get the collection
            col.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

if __name__ == '__main__':
    FILE_PATH = r"Network_Data\phisingData.csv"  # Use raw string to avoid escape issues
    DATABASE = "nabaranjan90"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    
    print(f"Records to insert: {len(records)}")
    
    if records:
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"Inserted {no_of_records} records into MongoDB.")
    else:
        print("No records found.")
