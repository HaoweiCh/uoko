import pymongo.database
import pymongo.collection

client = pymongo.MongoClient('mongodb://localhost:27017/')

db: pymongo.database.Database = client["Rent"]
collection: pymongo.collection.Collection = db["uoko"]

