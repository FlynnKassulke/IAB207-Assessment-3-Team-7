from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)
MyAccount_bp = Blueprint('MyAccount', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/event-details')
def event_details():
    return render_template('Event Details.html')

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