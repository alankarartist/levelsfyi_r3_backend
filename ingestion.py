import pandas as pd
import requests
from pymongo import MongoClient
import io

# Setup MongoDB connection
client = MongoClient('mongodb://db:27017/')
db = client['sensor_db']
collection = db['sensor_data']

def ingest_data(url):
    # Download the CSV file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error if the request fails

    # Validate file size (max 5GB)
    file_size = int(response.headers.get('Content-Length', 0))
    if file_size > 5 * 1024 * 1024 * 1024:
        raise Exception("File size exceeds 5GB limit")

    # Read the CSV into a Pandas DataFrame
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    record_count = len(df)

    # Validate record count (max 10M records)
    if len(df) > 10000000:
        raise Exception("CSV contains more than 10M records")

    # Check current record count in the collection
    current_count = collection.count_documents({})

    # Check if the total count would exceed the maximum allowed records
    if current_count + record_count > 50000000:
        raise Exception("Ingestion would exceed the maximum allowed records of 50 million")

    # Ensure column names match the required structure
    required_columns = ['id', 'type', 'subtype', 'reading', 'location', 'timestamp']
    if not all(column in df.columns for column in required_columns):
        raise Exception("CSV columns do not match required structure")

    # Convert DataFrame to dictionary format suitable for MongoDB
    records = df.to_dict(orient='records')

    # Insert data into MongoDB
    collection.insert_many(records)
