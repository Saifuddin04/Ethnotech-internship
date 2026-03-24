from flask_login import UserMixin
from db.mongo import users

class User(UserMixin):

    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.password = user_data["password"]

    @staticmethod
    def get(user_id):
        from bson.objectid import ObjectId
        user = users.find_one({"_id": ObjectId(user_id)})
        return User(user) if user else None