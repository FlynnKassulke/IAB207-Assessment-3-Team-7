from flask import Flask, Blueprint, render_template, session, redirect, request 
from werkzeug.security import generate_password_hash

app = Flask(__name__)
main_bp = Blueprint('main', __name__)
MyAccount_bp = Blueprint('MyAccount', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# Define the event_details route
@main_bp.route('/event-details')
def event_details():
    # Fetch quantities from session
    quantities = session.get('quantities', {
        "standard-adult": 0,
        "standard-concession": 0,
        "vip-seasons-package": 0,
        "vip-flumed": 0
    })

    # Calculate total costs
    ticket_prices = {
        "standard-adult": 152.68,
        "standard-concession": 877.55,
        "vip-seasons-package": 1412.78,
        "vip-flumed": 1682.95
    }
    total_ticket_cost = sum(quantities[ticket] * ticket_prices[ticket] for ticket in quantities)
    booking_fee = 10
    final_cost = total_ticket_cost + booking_fee

    # Render the template with quantities and costs
    return render_template('Event Details.html', quantities=quantities, total_ticket_cost=total_ticket_cost, final_cost=final_cost)

@main_bp.route('/event-creation')
def event_creation():
    return render_template('Event Creation.html')

@main_bp.route('/my-account')
def my_account():
    return render_template('My Account.html')

@main_bp.route('/login')
def login():
    return render_template('Login Page.html')

@main_bp.route('/register', methods =["GET","POST"])
def register():
    if request.method == "POST":
        user_name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        contact_number = request.form.get("contact_number")
        street_address = request.form.get("street_address")

        if not (user_name and email and password and contact_number and street_address):
            return render_template('Register Page.html', message="All fields are required")
        
        hashed_pass = generate_password_hash(password)

        return redirect('/login')

    return render_template('Register Page.html')