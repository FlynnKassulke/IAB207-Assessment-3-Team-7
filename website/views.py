from flask import Blueprint, render_template, session

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

@main_bp.route('/register')
def register():
    return render_template('Register Page.html')