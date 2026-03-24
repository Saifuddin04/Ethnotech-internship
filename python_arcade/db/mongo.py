from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)

# connect to database
db = client[Config.DB_NAME]

# collections (auto-created when used)
users = db["users"]
quiz_questions = db["quiz"]
scores = db["scores"]

# print("✅ Connected to MongoDB")