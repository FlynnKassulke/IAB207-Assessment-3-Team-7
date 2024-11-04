from flask import Flask, Blueprint, render_template, session, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash
from flask import render_template, request
from datetime import datetime
from .models import Event
#from . import main_bp
from flask import Blueprint, render_template, session, request, redirect, url_for
from .models import db, Event

app = Flask(__name__)
main_bp = Blueprint('main', __name__)
MyAccount_bp = Blueprint('MyAccount', __name__)

@main_bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@main_bp.route('/event/', methods=['GET'])
def event_details():
    event = Event.query.get_or_404()
    quantities = session.get('quantities', {
        "standard-adult": 0,
        "standard-concession": 0,
        "vip-seasons-package": 0
    })

    ticket_prices = {
        "standard-adult": 152.68,
        "standard-concession": 877.55,
        "vip-seasons-package": 1412.78
    }
    total_ticket_cost = sum(quantities[ticket] * ticket_prices[ticket] for ticket in quantities)
    booking_fee = 10
    final_cost = total_ticket_cost + booking_fee

    return render_template(
        'Event Details.html',
        event=event,
        quantities=quantities,
        total_ticket_cost=total_ticket_cost,
        final_cost=final_cost
    )

@main_bp.route('/events', methods=['GET'])
def events():
    sort_criteria = request.args.get('sort', '')
    print("Received sort criteria:", sort_criteria)  # Debugging log

    # Base query
    query = Event.query

    # Apply sorting based on selected criteria
    if sort_criteria == 'genre':
        query = query.order_by(Event.genre)
    elif sort_criteria == 'date':
        query = query.order_by(Event.time)

    # Execute query to get the events
    events = query.all()

    # Add current datetime to context
    now = datetime.now()
    
    # Render template with sorted events and 'now' for date comparisons
    return render_template('index.html', events=events, now=now)


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

# Define index and event details route as before

@main_bp.route('/increment/<ticket_type>')
def increment(ticket_type):
    quantities = session.get('quantities', {})
    ticket_limits = {
        "standard-adult": None,
        "standard-concession": 2,
        "vip-seasons-package": 2
    }
    if ticket_type in quantities and (ticket_limits[ticket_type] is None or quantities[ticket_type] < ticket_limits[ticket_type]):
        quantities[ticket_type] += 1
        session['quantities'] = quantities
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/decrement/<ticket_type>')
def decrement(ticket_type):
    quantities = session.get('quantities', {})
    if ticket_type in quantities and quantities[ticket_type] > 0:
        quantities[ticket_type] -= 1
        session['quantities'] = quantities
    return redirect(request.referrer or url_for('main.index'))