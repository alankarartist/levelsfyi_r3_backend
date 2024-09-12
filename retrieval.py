from pymongo import MongoClient
import numpy as np

# Setup MongoDB connection
client = MongoClient('mongodb://db:27017/')
db = client['sensor_db']
collection = db['sensor_data']

def get_median(filters):
    # Build MongoDB query based on filters
    query = {}
    
    # Apply filters if provided
    if 'id' in filters:
        query['id'] = {'$in': filters['id']}
    if 'type' in filters:
        query['type'] = {'$in': filters['type']}
    if 'subtype' in filters:
        query['subtype'] = {'$in': filters['subtype']}
    if 'location' in filters:
        query['location'] = {'$in': filters['location']}

    # Retrieve matching sensor readings
    readings = list(collection.find(query, {'reading': 1, '_id': 0}))
    readings = [item['reading'] for item in readings]

    # Compute the median of the readings
    median = np.median(readings) if readings else 0
    return {"count": len(readings), "median": median}
