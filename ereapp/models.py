from datetime import datetime
from bson.objectid import ObjectId


class UserModel:
    @staticmethod
    def create(fullname, phone, username, password, question=None, answer=None):
        return {
            "fullname": fullname,
            "phone": phone,
            "username": username,
            "password": password,
            "security": {
                "question": question,
                "answer": answer
            } if question and answer else None,
            "created_at": datetime.utcnow()
        }

class AdminModel:
    @staticmethod
    def create(fname, lname, username, password):
        return {
            "fname": fname,
            "lname": lname,
            "username": username,
            "password": password,
            "created_at": datetime.utcnow()
        }

class ContactModel:
    @staticmethod
    def create(name, email, phone, gender, method, message):
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "method": method,
            "message": message,
            "status": "new",  # new, read, resolved
            "handled_by": None,
            "created_at": datetime.utcnow()
        }

class TourModel:
    @staticmethod
    def create(name, description, price, image, start_date, end_date):
        return {
            "name": name,
            "description": description,
            "price": float(price),
            "image": image,
            "start_date": start_date,
            "end_date": end_date,
            "created_at": datetime.utcnow()
        }

class TripModel:
    @staticmethod
    def create(user_id, tour):
        return {
            "user_id": ObjectId(user_id),

            "tour": {
                "id": tour["_id"],
                "name": tour["name"],
                "price": tour["price"],
                "start_date": tour.get("start_date")
            },

            "payment": {
                "amount": tour["price"],
                "status": "pending",  # pending, paid, failed
                "receipt": None,
                "paid_at": None
            },

            "status": "booked",  # booked, confirmed, completed
            "created_at": datetime.utcnow()
        }

    @staticmethod
    def mark_paid():
        return {
            "$set": {
                "payment.status": "paid",
                "payment.paid_at": datetime.utcnow(),
                "status": "confirmed"
            }
        }

class EmailModel:
    @staticmethod
    def create(email):
        return {
            "email": email,
            "created_at": datetime.utcnow()
        }