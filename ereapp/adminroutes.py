import os, random, string
from datetime import datetime
from flask import render_template, request, redirect, session, flash
from bson.objectid import ObjectId
from ereapp import starter
from ereapp.services.admin_services import AdminService


# Helpers
def generate_name():
    return ''.join(random.sample(string.ascii_lowercase, 10))


# Auth
@starter.route('/admin/signup', methods=["GET", "POST"])
def adminsignup():
    if request.method == "POST":
        result = AdminService.create_admin(
            request.form.get("fname"),
            request.form.get("lname"),
            request.form.get("username"),
            request.form.get("password")
        )

        if "error" in result:
            flash(result["error"], "danger")
            return redirect("/admin/signup")

        flash("Account created!", "success")
        return redirect("/admin/login")

    return render_template('admin/adminsignup.html')


@starter.route('/admin/login', methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        result = AdminService.login_admin(
            request.form.get("username"),
            request.form.get("password")
        )

        if "error" in result:
            flash(result["error"], "danger")
            return redirect("/admin/login")

        session["admin"] = str(result["admin"]["_id"])
        return redirect("/admin")

    return render_template('admin/adminlogin.html')


@starter.route('/admin/logout')
def adminlogout():
    session.pop("admin", None)
    return redirect("/admin/login")


# Dashboard
@starter.route('/admin')
def adminhome():
    if not session.get("admin"):
        return redirect("/admin/login")

    trips = AdminService.get_all_trips()
    return render_template("admin/admindashboard.html", mdeets=trips)


# Contacts
@starter.route("/admin/messages")
def messages():
    if not session.get("admin"):
        return redirect("/admin/login")

    contacts = AdminService.get_new_contacts()
    return render_template("admin/inview.html", mdeets=contacts)


@starter.route("/admin/sort/<contact_id>")
def sort(contact_id):
    AdminService.mark_contact_resolved(contact_id)
    return redirect("/admin/messages")


@starter.route("/admin/sorted")
def sorted():
    contacts = AdminService.get_all_contacts()
    return render_template("admin/sorted.html", mdeets=contacts)


# Tours
@starter.route("/admin/tours", methods=["GET", "POST"])
def admintours():
    if not session.get("admin"):
        return redirect("/admin/login")

    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        price = request.form.get("price")
        start = datetime.strptime(request.form['startdate'], '%Y-%m-%d')
        end = datetime.strptime(request.form['enddate'], '%Y-%m-%d')

        img = request.files['img']
        filename = img.filename

        if filename:
            name, ext = os.path.splitext(filename)
            newname = generate_name() + ext
            img.save(f"ereapp/static/uploads/{newname}")
        else:
            flash("Please choose a file")
            return redirect(request.referrer)

        AdminService.create_tour(title, desc, price, newname, start, end)

        flash("Tour created successfully", "success")
        return redirect("/admin/tours")

    tours = AdminService.get_all_tours()
    return render_template('admin/tourpost.html', mdeets=tours)


@starter.route("/admin/deletetour/<tour_id>")
def deletetour(tour_id):
    AdminService.delete_tour(tour_id)
    return redirect("/admin/tours")