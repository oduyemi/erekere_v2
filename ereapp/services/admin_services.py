from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ereapp import mongo
from ereapp.models import AdminModel, TourModel


class AdminService:

    @staticmethod
    def create_admin(fname, lname, username, password):
        existing = mongo.db.admins.find_one({"username": username})
        if existing:
            return {"error": "Admin already exists"}

        admin = AdminModel.create(
            fname, lname, username,
            generate_password_hash(password)
        )

        result = mongo.db.admins.insert_one(admin)
        return {"success": True, "admin_id": str(result.inserted_id)}


    @staticmethod
    def login_admin(username, password):
        admin = mongo.db.admins.find_one({"username": username})

        if not admin:
            return {"error": "Admin not found"}

        if not check_password_hash(admin["password"], password):
            return {"error": "Invalid password"}

        return {"success": True, "admin": admin}


    @staticmethod
    def get_all_contacts():
        return list(mongo.db.contacts.find().sort("created_at", -1))


    @staticmethod
    def get_new_contacts():
        return list(mongo.db.contacts.find({"status": "new"}))


    @staticmethod
    def mark_contact_resolved(contact_id):
        mongo.db.contacts.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": {"status": "resolved"}}
        )


    @staticmethod
    def create_tour(title, desc, price, image, start, end):
        tour = TourModel.create(title, desc, price, image, start, end)
        mongo.db.tours.insert_one(tour)


    @staticmethod
    def get_all_tours():
        return list(mongo.db.tours.find().sort("created_at", -1))


    @staticmethod
    def delete_tour(tour_id):
        mongo.db.tours.delete_one({"_id": ObjectId(tour_id)})


    @staticmethod
    def get_all_trips():
        return list(mongo.db.trips.find().sort("created_at", -1))