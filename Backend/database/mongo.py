from pymongo import MongoClient
from Backend.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client["Aashraydatabase"]