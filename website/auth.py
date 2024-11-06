from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from flask import Flask


app = Flask(__name__)
# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=["GET", "POST"])
# view function
def login():
 if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password_hash")
        
        # Print statements for debugging
        print("name:", name)
        print("Password:", password)

        if not name or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")

        user = User.query.filter_by(name=name).first()
        print("User:", user)

        if user is None:
            flash("No account found with that username.", "error")
            return render_template("login.html")

        if not check_password_hash(user.password_hash, password):
            flash("Incorrect password. Please try again.", "error")
            return render_template("login.html")

        login_user(user)
        flash("Login successful!", "success")

        next_page = request.args.get("next")
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("index")
        
        return redirect(next_page)

        return render_template("login.html")


#logout function
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
