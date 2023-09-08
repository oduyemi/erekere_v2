import os, random, string
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from sqlalchemy.sql import text
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from ereapp import starter, db
from ereapp.models import User, Contact, Payment, Tour, Trip, Question


def generate_name():
    global filename
    filename = random.sample(string.ascii_lowercase,10)
    return ''.join(filename) 

#       --  ERROR HANDLERS  --
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
    else:
        return render_template("error405.html"), 405    




#       --  ROUTES  --
@starter.route('/', strict_slashes = False)
def home():
    return render_template('user/index.html')


@starter.route('/contact', methods = ["POST", "GET"], strict_slashes = False)
def contact():
    if request.method == "POST":
        c_name = request.form.get("c_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        gender=request.form.get("gender")
        method=request.form.get("method")
        message=request.form.get("message")
        if c_name !='' and phone != "" and email !='' and gender !='' and method != "" and message != "":
            new_contact=Contact(contact_name = c_name, contact_phone = phone, contact_email = email, contact_gender = gender, contact_method = method, contact_content = message, contact_status_id=1)
            db.session.add(new_contact)
            db.session.commit()
            flash(f"Thank you for reaching out to us, We will get in touch with you shortly. ", "success")
            return redirect(url_for("contact"))
        else:
            flash(f"Please fill all fields", "danger")
            return redirect(request.referrer)
    else:
        return render_template('user/contact.html')


@starter.route('/about', strict_slashes = False)
def about():
    return render_template('user/about.html')

@starter.route('/signup', methods = ["POST", "GET"], strict_slashes = False)
def usersignup():
    if request.method == "GET":
        return render_template('user/signup.html', title="Sign Up")
    else:
        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        username = request.form.get("username")
        password=request.form.get("password")
        hashedpwd = generate_password_hash(password)
        if fullname !='' and phone != "" and username !='' and password !='':
            new_user=User(user_fullname = fullname, user_phone = phone, user_username = username,
            user_password = hashedpwd)
            db.session.add(new_user)
            db.session.commit()
            userid=new_user.user_id
            session['user']=userid
            flash(f"Account created for '{fullname}'! Please proceed to LOGIN ", "success")
            return redirect(url_for('userlogin'))
        else:
            flash('You must fill the form correctly to signup', "danger")
    # return render_template('user/signup.html')


@starter.route('/login', methods = ['POST', 'GET'], strict_slashes = False)
def userlogin():
    if request.method=='GET':
        return render_template('user/login.html')
    else:
        username=request.form.get('username')
        pwd=request.form.get('password')
        deets = db.session.query(User).filter(User.user_username==username).first() 
        if deets !=None:
            pwd_indb = deets.user_password
            chk = check_password_hash(pwd_indb, pwd)
            if chk:
                id = deets.user_id
                session['user'] = id
                return redirect(url_for('account'))
            else:
                flash('Invalid password')
        return redirect(url_for('userlogin'))


@starter.route('/reset', methods = ['POST', 'GET'], strict_slashes = False)
def passwordreset():
    if request.method=='GET':
        return render_template('user/login.html')
    else:
        username=request.form.get('username')


@starter.route("/logout", strict_slashes = False)
def userlogout():
    if session.get("user") != None:
        session.pop("user",None)
    return redirect('/login')

                    

@starter.route('/media', strict_slashes = False)
def media():
    return render_template('user/media.html')

@starter.route('/account', strict_slashes = False)
def account():
    id=session.get("user")
    mdeets =  db.session.query(Trip).where(Trip.trip_user==id).all()
    if session.get("user") != None:
        return render_template('user/myaccount.html', mdeets=mdeets)
    else:
        return redirect(url_for("userlogin"))


@starter.route('/secret', methods=["GET", "POST"],strict_slashes = False)
def secret():
    id=session.get("user")
    qfeeds = db.session.query(Question).order_by(Question.question_id).all()
    deets =  db.session.query(User).where(User.user_id==id).first()
    #db.session.query(Business).join(B_user, Business.bdeets).where(Business.business_userid==cid).first()
    #mdeets = db.session.execute(text(query))
    if request.method == "POST":
        if session.get('user') != None:
            quest=request.form.get("quest")
            rsp=request.form.get("secret")
            query=f"UPDATE user SET user_question='{quest}', user_secret='{rsp}' WHERE user_id='{id}'"
            db.session.execute(text(query))
            try:
                db.session.commit()
                return redirect(url_for('secret'))
            
            except:
                return redirect(url_for('secret'))
    return render_template('user/secret.html', deets=deets, qfeeds=qfeeds, id=id)


    
        


@starter.route('/alltrips', strict_slashes = False)
def Trips():
    id=session.get("user")
    mdeets =  db.session.query(Tour).all()
    #mdeets = db.session.execute(text(query))
    return render_template('user/alltrips.html', mdeets=mdeets)

@starter.route('/pending', strict_slashes = False)
def pending():
    id=session.get("user")
    mdeets =  db.session.query(Payment).where(Payment.payment_user==id, Payment.payment_status==1).all()
    #mdeets = db.session.execute(text(query))
    return render_template('user/pending.html', mdeets=mdeets)

@starter.route('/previous', strict_slashes = False)
def previous():
    id=session.get("user")
    # now = SELECT GETDATE()
    mdeets = db.session.query(Trip).filter(Trip.trip_user==id, getdate()-Trip.tripdeets.tour_enddate <= 0)
    # query =  f"SELECT * FROM trip WHERE trip_user='{id}' AND (NOW() - tripdeets.tour_enddate <= 0)"
    # mdeets = db.session.execute(text(query))
    return render_template('user/previous.html', mdeets=mdeets)

@starter.route('/tours', methods=["GET", "POST"], strict_slashes = False)
def tours():
    id = session.get("user")
    tour = db.session.query(Tour).order_by(Tour.tour_id.desc()).all()
    if id != None:
        if request.method == "POST":
            tname = request.form.get("tname")
            tripreg = Trip(trip_tour=tname, trip_user=id, trip_payment_status=1)
            trippay = Payment(payment_status=1, payment_user=id, payment_trip=tname, payment_date="")
            db.session.add(tripreg)
            db.session.add(trippay)
            db.session.commit()
            return redirect("/pay")
        return render_template('user/tours.html',tour=tour)
    else:
        return render_template('user/tours.html',tour=tour)

@starter.route('/trip', strict_slashes = False)
def trip():
    return render_template('user/trip.html')

@starter.route('/privacy-policy', strict_slashes = False)
def privacypolicy():
    return render_template('user/privacy-policy.html')

@starter.route('/site-requirements', strict_slashes = False)
def siterequirements():
    return render_template('user/site-requirements.html')

@starter.route('/terms-conditions', strict_slashes = False)
def termsandcondition():
    return render_template('user/terms-and-conditions.html')

@starter.route("/pay", methods=["POST","GET"], strict_slashes = False)
def payment():
    id = session.get("user")
    #item=Tour.query.get_or_404(id)
    qfeeds = db.session.query(Tour).order_by(Tour.tour_id).all()
    if id != None:
        if request.method == "POST":
            amount = request.form.get("amount")
            fullname = request.form.get("fullname")
            dtrip = request.form.get("dtrip")
            pupdate =  f"INSERT INTO payment (payment_name, payment_amount, payment_trip, payment_user, payment_status) VALUES('{fullname}','{amount}', '{dtrip}', '{id}', 1) WHERE trip_id='{item}'"
            db.session.add(pupdate)
            tupdate = f"UPDATE trip SET trip_payment_status=2, trip_tour='{dtrip}' WHERE trip_tour='{dtrip}'"
            db.session.execute(text(tupdate))
            db.session.commit()
            return redirect("/confirm")
        else:
            return render_template("user/payment.html", qfeeds=qfeeds, id=id)
    else:
        return redirect(url_for("userlogin"))


@starter.route("/confirm", methods=["POST","GET"])
def confirm():
    id=session.get("user")
    p=db.session.query(Payment).all()
    if request.method=="POST":
        if id != None:
            ctrip=request.form.get("c_trip")
            receipt=request.files['receipt']
            filename = receipt.filename 
            filetype = receipt.mimetype
            allowed= ['.png','.jpg','.jpeg', ".webp", '.pdf'] 
            if filename !="":
                name,ext = os.path.splitext(filename) 
                if ext.lower() in allowed: 
                    newname = generate_name()+ext
                    receipt.save("ereapp/static/uploads/"+newname) 
                else:
                    return "File not allowed!"
            else:
                flash("Please choose a File")
            query = f"UPDATE trip SET trip_receipt='{newname}', trip_payment_status=1 WHERE trip_user='{id}' AND trip_id='{ctrip}'"
            db.session.execute(text(query))
            c1 = f"UPDATE payment SET payment_status=1 WHERE payment_user='{id}'"
            db.session.execute(text(c1))
            c2 = f"UPDATE trip SET trip_payment_status=1 WHERE trip_user='{id}'"
            db.session.execute(text(c2))
            db.session.commit()
            flash("You have successfully completed the booking process", "success")
            return redirect("/account")
    else:
        p = db.session.query(Payment).where(Payment.payment_user==id).first()
        return render_template("user/confirmation.html", p=p)



          