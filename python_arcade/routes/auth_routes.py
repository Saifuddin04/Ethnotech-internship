from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db.mongo import users
from models.user_model import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = users.find_one({"username": username})

        if user and check_password_hash(user["password"], password):

            login_user(User(user))
            return redirect(url_for("game.dashboard"))

    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        existing_user = users.find_one({"username": username})

        if existing_user:
            return "User already exists. Please login."

        users.insert_one({
            "username": username,
            "password": password,
            "wins": 0
        })

        return redirect(url_for("auth.login"))

    return render_template("signup.html")
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/")