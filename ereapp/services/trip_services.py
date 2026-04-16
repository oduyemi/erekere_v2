from datetime import datetime
from bson.objectid import ObjectId
from ereapp import mongo
from ereapp.models import TripModel


class TripService:

    @staticmethod
    def book_trip(user_id, tour_id):
        tour = mongo.db.tours.find_one({"_id": ObjectId(tour_id)})

        if not tour:
            return {"error": "Tour not found"}

        trip_data = TripModel.create(user_id, tour)

        result = mongo.db.trips.insert_one(trip_data)

        return {"success": True, "trip_id": str(result.inserted_id)}


    @staticmethod
    def get_user_trips(user_id):
        return list(mongo.db.trips.find({
            "user_id": ObjectId(user_id)
        }).sort("created_at", -1))


    @staticmethod
    def mark_trip_paid(trip_id):
        result = mongo.db.trips.update_one(
            {"_id": ObjectId(trip_id)},
            TripModel.mark_paid()
        )

        if result.modified_count == 0:
            return {"error": "Trip not found or already updated"}

        return {"success": True}


    @staticmethod
    def upload_receipt(trip_id, filename):
        mongo.db.trips.update_one(
            {"_id": ObjectId(trip_id)},
            {
                "$set": {
                    "payment.receipt": filename
                }
            }
        )

        return {"success": True}


    @staticmethod
    def get_all_trips():
        return list(mongo.db.trips.find().sort("created_at", -1))