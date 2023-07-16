from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from extensions import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("The email does not exist in the database!")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # Cookie：
                # Cookies are not suitable for storing too much data, only suitable for storing a small amount of data
                # Cookies are generally used to store login authorization
                # The session in flask is encrypted and stored in cookie
                session['user_id'] = user.id  # key-value pair
                return redirect("/")
            else:
                print("Wrong password!")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET：Get data from the server
# POST：Submit client data to server
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # Verify that the email address and the corresponding verification code submitted by the user are correct
        # Form Validation：flask-wtf: wtforms
        form = RegisterForm(request.form)  # "RegisterForm" is a class, "form" is an object here
        if form.validate():  # will invoke all the validators and validate functions
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # Build a new user object
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # return "Login Successfully"
            # return redirect(url_for("/auth/login"))
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            # return "Login Failed"
            return redirect(url_for("auth.register"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# bp.route：If the methods parameter is not specified, the default is a GET request
@bp.route("/captcha/email")
def get_email_captcha():
    # Get Parameters:
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    # 4/6：Combination of random arrays, letters, arrays and letters
    # source = '0123456789012345678901234567890123456789'
    source = string.digits * 4
    captcha = random.sample(source, 4)
    # transform list to str
    captcha = "".join(captcha)
    # I/O：Input/Output operation, could be time-consuming, better do it asynchronously in another request
    # Send the Registration Verification Code
    message = Message(subject="QA Platform Registration Verification Code", recipients=[email],
                      body=f"Your Verification Code is: {captcha}")
    mail.send(message)
    # memcached/redis for production purpose. save verification codes in server cache.
    # for study purpose now, stored in a database table
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code: 200/400/500, message: "", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message("Mail Test 2", recipients=["xyi@scu.edu"], body="This is a test mail.")
    mail.send(message)
    return "Mail sent successfully"
