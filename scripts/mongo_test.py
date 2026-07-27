import sys, os
sys.path.insert(0, os.getcwd())
from app.backend import config
from pymongo import MongoClient

def main():
    print('Using MONGO_URL:', config.settings.MONGO_URL)
    client = MongoClient(config.settings.MONGO_URL, serverSelectionTimeoutMS=5000)
    try:
        info = client.server_info()
        print('server_info:', info.get('version'))
        print('databases:', client.list_database_names())
    except Exception as e:
        print('connect error:', repr(e))
        print('attempting fallback with tlsAllowInvalidCertificates=True')
        try:
            client2 = MongoClient(config.settings.MONGO_URL, serverSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=True)
            info2 = client2.server_info()
            print('fallback server_info:', info2.get('version'))
            print('fallback databases:', client2.list_database_names())
        except Exception as e2:
            print('fallback error:', repr(e2))
            try:
                import certifi
                print('attempting with certifi CA bundle')
                client3 = MongoClient(config.settings.MONGO_URL, serverSelectionTimeoutMS=5000, tls=True, tlsCAFile=certifi.where())
                info3 = client3.server_info()
                print('certifi server_info:', info3.get('version'))
                print('certifi databases:', client3.list_database_names())
            except Exception as e3:
                print('certifi fallback error:', repr(e3))

if __name__ == '__main__':
    main()
