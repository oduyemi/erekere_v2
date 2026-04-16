import os, random, string
from datetime import datetime
from flask import render_template, request, redirect, session, flash, jsonify
from flask_wtf import CSRFProtect
from bson.objectid import ObjectId
from ereapp import starter
from ereapp.services.user_services import UserService
from ereapp.services.trip_services import TripService

csrf = CSRFProtect(starter)

def generate_name():
    return ''.join(random.sample(string.ascii_lowercase, 10))



@starter.errorhandler(404)
def page_not_found(e):
    return render_template("user/error404.html"), 404


@starter.errorhandler(500)
def internal_server_error(e):
    return render_template("error500.html"), 500


@starter.errorhandler(405)
def method_not_allowed(e):
    if request.path.startswith('/api/'):
        return jsonify(message="Method Not Allowed"), 405
    return render_template("error405.html"), 405


# Routes
@starter.route('/')
def home():
    return render_template('user/index.html')


@starter.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        from ereapp.models import ContactModel
        from ereapp import mongo

        data = request.form

        mongo.db.contacts.insert_one(
            ContactModel.create(
                name=data.get("c_name"),
                email=data.get("email"),
                phone=data.get("phone"),
                gender=data.get("gender"),
                method=data.get("method"),
                message=data.get("message")
            )
        )

        flash("Message sent!", "success")
        return redirect("/contact")

    return render_template("user/contact.html")


@starter.route('/about')
def about():
    return render_template('user/about.html')


# Auth
@starter.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = UserService.login_user(
            request.form.get("username"),
            request.form.get("password")
        )

        if "error" in result:
            flash(result["error"], "danger")
            return redirect("/login")

        session["user"] = str(result["user"]["_id"])
        return redirect("/my-trips")

    return render_template("user/login.html")


@starter.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")


# Tours
@starter.route("/tours")
def tours():
    from ereapp import mongo
    tours = list(mongo.db.tours.find().sort("created_at", -1))
    return render_template("user/tours.html", tour=tours)


# Booking
@starter.route("/book", methods=["POST"])
def book_trip():
    user_id = session.get("user")

    if not user_id:
        return redirect("/login")

    result = TripService.book_trip(
        user_id,
        request.form.get("tour_id")
    )

    if "error" in result:
        flash(result["error"], "danger")
        return redirect("/tours")

    return redirect("/my-trips")


@starter.route("/pay/<trip_id>", methods=["POST"])
def pay(trip_id):
    result = TripService.mark_trip_paid(trip_id)

    if "error" in result:
        flash(result["error"], "danger")

    return redirect("/my-trips")


@starter.route("/my-trips")
def my_trips():
    user_id = session.get("user")

    if not user_id:
        return redirect("/login")

    trips = TripService.get_user_trips(user_id)

    return render_template("user/mytrips.html", trips=trips)


# Static Pages
@starter.route('/trip')
def trip():
    return render_template('user/trip.html')


@starter.route('/privacy-policy')
def privacypolicy():
    return render_template('user/privacy-policy.html')


@starter.route('/terms-conditions')
def termsandcondition():
    return render_template('user/terms-and-conditions.html')