from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from ereapp import mongo
from ereapp.models import UserModel


class UserService:

    @staticmethod
    def create_user(fullname, phone, username, password):
        # check if user exists
        existing = mongo.db.users.find_one({"username": username})
        if existing:
            return {"error": "User already exists"}

        hashed = generate_password_hash(password)

        user_data = UserModel.create(
            fullname=fullname,
            phone=phone,
            username=username,
            password=hashed
        )

        result = mongo.db.users.insert_one(user_data)

        return {"success": True, "user_id": str(result.inserted_id)}


    @staticmethod
    def login_user(username, password):
        user = mongo.db.users.find_one({"username": username})

        if not user:
            return {"error": "User not found"}

        if not check_password_hash(user["password"], password):
            return {"error": "Invalid password"}

        return {"success": True, "user": user}


    @staticmethod
    def get_user(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})


    @staticmethod
    def get_all_users():
        return list(mongo.db.users.find())