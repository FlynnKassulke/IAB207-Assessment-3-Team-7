# import flask - from 'package' import 'Class'
from flask import Flask, session, redirect, url_for, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

# Ticket prices and limits
ticket_prices = {
    "standard-adult": 152.68,
    "standard-concession": 877.55,
    "vip-seasons-package": 1412.78,
    "vip-flumed": 1682.95
}

ticket_limits = {
    "standard-adult": None,  # No limit
    "standard-concession": 2,
    "vip-seasons-package": 2,
    "vip-flumed": 2
}

# Default ticket quantities
default_quantities = {
    "standard-adult": 0,
    "standard-concession": 0,
    "vip-seasons-package": 0,
    "vip-flumed": 0
}

# Create a function that creates a web application
# A web server will run this web application
def create_app():
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug = True
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
    db.init_app(app)

    Bootstrap5(app)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Create a user loader function takes userid and returns User
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))
    
    @app.context_processor
    def inject_quantities():
        quantities = session.get('quantities', {
            "standard-adult": 0,
            "standard-concession": 0,
            "vip-seasons-package": 0,
            "vip-flumed": 0
        })
        ticket_prices = {
            "standard-adult": 152.68,
            "standard-concession": 877.55,
            "vip-seasons-package": 1412.78,
            "vip-flumed": 1682.95
        }
        total_ticket_cost = sum(quantities[ticket] * ticket_prices[ticket] for ticket in quantities)
        booking_fee = 10
        final_cost = total_ticket_cost + booking_fee

        return {
            'quantities': quantities,
            'total_ticket_cost': total_ticket_cost,
            'final_cost': final_cost
        }

    # Initialize ticket quantities in the session if they don't exist
    @app.before_request
    def initialize_quantities():
        if 'quantities' not in session:
            session['quantities'] = default_quantities.copy()

            # Main route to display tickets and costs
    @app.route('/')
    def index():
        quantities = session.get('quantities', default_quantities)
        total_ticket_cost = sum(quantities[ticket] * ticket_prices[ticket] for ticket in quantities)
        total_ticket_cost = round(total_ticket_cost, 2)
        booking_fee = 10
        final_cost = total_ticket_cost + booking_fee
        final_cost = round(final_cost, 2)
        return render_template('index.html', quantities=quantities, total_ticket_cost=total_ticket_cost, final_cost=final_cost)

    # Main route to display tickets and costs
    @app.route('/')
    def eventDetails():
        quantities = session.get('quantities', default_quantities)
        total_ticket_cost = sum(quantities[ticket] * ticket_prices[ticket] for ticket in quantities)
        total_ticket_cost = round(total_ticket_cost, 2)
        booking_fee = 10
        final_cost = total_ticket_cost + booking_fee
        final_cost = round(final_cost, 2)
        return render_template('Event Details.html', quantities=quantities, total_ticket_cost=total_ticket_cost, final_cost=final_cost)

    # Route to increment ticket quantity
    @app.route('/increment/<ticket_type>')
    def increment(ticket_type):
        if ticket_limits[ticket_type] is None or session['quantities'][ticket_type] < ticket_limits[ticket_type]:
            session['quantities'][ticket_type] += 1
        session.modified = True
        return redirect(url_for('main.event_details'))

    # Route to decrement ticket quantity
    @app.route('/decrement/<ticket_type>')
    def decrement(ticket_type):
        if session['quantities'][ticket_type] > 0:
            session['quantities'][ticket_type] -= 1
        session.modified = True
        return redirect(url_for('main.event_details'))

    # Register blueprints
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)
    
    return app
