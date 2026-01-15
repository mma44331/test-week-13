import os
import pymongo
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError, ConnectionFailure
from dotenv import load_dotenv
load_dotenv()


def get_con_mongo():
    try:
        client = pymongo.MongoClient(
            host=os.getenv("MONGO_HOST"),
            port=int(os.getenv("MONGO_PORT")),
            username=os.getenv("MONGO_USERNAME"),
            password=os.getenv("MONGO_PASSWORD"),
            authSource=os.getenv("MONGO_AUTH_SOURCE"),
            serverSelectionTimeoutMS=3000
        )

        client.admin.command("ping")
        return client
    except PyMongoError as err:
        if isinstance(err, ServerSelectionTimeoutError):
            print("Cannot connect to MongoDB server")
        elif isinstance(err, ConnectionFailure):
            print("MongoDB connection failed")
        else:
            print(err)
        return None

def get_db(client):
    db_name = os.getenv("MONGO_DB")
    if not db_name:
        raise ValueError("MONGO_DB is not set")
    return client[db_name]


def get_col(db):
    col_name = os.getenv("MONGO_COLACTION")
    if not col_name:
        raise ValueError("MONGO_COLACTION is not set")
    return db[col_name]



def get_col_threat():
    client = get_con_mongo()
    if client is None:
        return None
    db = get_db(client)
    col = get_col(db)
    return col



class Threads():
    def __init__(self):
        self.col = get_col_threat()
        if self.col is None:
            raise ConnectionError("Cannot connect to the database")


    def get_threats(self) -> dict:
        try:
            doc = self.col.find_one(sort=[("_id", -1)])  # המסמך האחרון
            if not doc:
                return {"count": 0, "top": []}
            doc.pop("_id", None)
            return doc
        except PyMongoError as err:
            print(f"Error db {err}")
            return {"error": str(err)}

    def create_new_threat(self, threats) -> dict:
        print("Received threats:", threats)

        try:
            data = {
                "count": threats["count"],
                "top": threats["top"]
            }
            self.col.insert_one(data)
            return {"message": "threats created successfully"}
        except PyMongoError as err:
            print(f"Error db {err}")
            return {"error": str(err)}

