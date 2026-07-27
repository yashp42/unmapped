import sys
import os
sys.path.insert(0, os.getcwd())

from app.backend import config
from pymongo import MongoClient

COLLECTION = 'integration_test_unmapped'

def main():
    url = os.environ.get('MONGO_URL', config.settings.MONGO_URL)
    print('Using MONGO_URL:', url)
    client = MongoClient(url, serverSelectionTimeoutMS=10000)
    db = client[config.settings.DB_NAME]
    coll = db[COLLECTION]

    try:
        print('Checking server connection...')
        print('server version:', client.server_info().get('version'))
    except Exception as e:
        print('Connection failed:', repr(e))
        return

    try:
        print('Cleaning collection if exists...')
        coll.drop()

        print('Inserting document...')
        result = coll.insert_one({'name': 'integration-test', 'value': 1})
        print('Inserted id:', result.inserted_id)

        print('Reading document...')
        doc = coll.find_one({'_id': result.inserted_id})
        print('Found:', doc)

        print('Updating document...')
        coll.update_one({'_id': result.inserted_id}, {'$set': {'value': 2}})
        updated = coll.find_one({'_id': result.inserted_id})
        print('Updated:', updated)

        print('Deleting document...')
        coll.delete_one({'_id': result.inserted_id})
        deleted = coll.find_one({'_id': result.inserted_id})
        print('Deleted exists?', deleted is not None)

        print('Dropping collection...')
        coll.drop()
        print('CRUD test completed successfully.')
    except Exception as e:
        print('CRUD error:', repr(e))
    finally:
        client.close()

if __name__ == '__main__':
    main()
