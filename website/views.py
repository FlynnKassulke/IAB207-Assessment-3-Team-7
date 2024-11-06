from flask import Flask, Blueprint, render_template, session, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import Event, Comment, db, User
from .forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user

app = Flask(__name__)
main_bp = Blueprint('main', __name__)
MyAccount_bp = Blueprint('MyAccount', __name__)

@main_bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    quantities = session.get('quantities', {
        "standard-adult": 2,
        "standard-concession": 0,
        "vip-seasons-package": 0
    })

    # Define ticket prices here
    ticket_prices = {
        "standard-adult": 150,
        "standard-concession": 100,
        "vip-seasons-package": 500
    }
    total_ticket_cost = sum(quantities[ticket] * ticket_prices.get(ticket, 0) for ticket in quantities)
    booking_fee = 10
    final_cost = total_ticket_cost + booking_fee

    # Fetch comments for the event
    comments = Comment.query.filter_by(eventid=event_id).order_by(Comment.date_posted.desc()).all()

    if request.method == 'POST':
        # Get form data
        comment_text = request.form.get('comment')
        
        # Create a new Comment instance
        new_comment = Comment(
            comment=comment_text,
            date_posted=datetime.now(),
            eventid=event_id
            #userid=user_id
        )
        
        # Add and commit the new comment to the database
        db.session.add(new_comment)
        db.session.commit()
        
        return redirect(url_for('main.event_details', event_id=event_id))

    # Pass ticket_prices, comments, and other context variables to the template
    return render_template(
        'Event Details.html',
        event=event,
        quantities=quantities,
        ticket_prices=ticket_prices,
        total_ticket_cost=total_ticket_cost,
        final_cost=final_cost,
        comments=comments
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

@main_bp.route('/event-creation', methods=['GET', 'POST'])
def event_creation():
    if request.method == 'POST':
        print("Posting")
        # Collect form data
        title = request.form.get('title')
        venue = request.form.get('venue')
        description = request.form.get('description')
        genre = request.form.get('genre')
        artist = request.form.get('artist')
        event_time = request.form.get('when')
        contact_number = request.form.get('contact_number')
        street_address = request.form.get('street_address')
        status = "Open"

        # Convert date/time to datetime object
        try:
            event_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M')  # Adjust the format to match the HTML datetime-local format
        except ValueError:
            flash("Incorrect date format. Please use 'YYYY-MM-DD HH:MM'")
            return redirect(url_for('main.event_creation'))
        
        


        # Create and save the new event
        new_event = Event(
            name=title,
            description=description,
            genre=genre,
            photo="/img/HitsOnDeckLogo.jpg",  # Placeholder or default image path
            status="Open",  # Default status
            location=venue,
            time=event_time,  # Now a datetime object
            contact_number=contact_number,
            street_address=street_address
        )

        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!')
        return redirect(url_for('main.index'))

    return render_template('Event Creation.html')

@main_bp.route('/my-account')
def my_account():
    events = Event.query.all()  # Query all events
    return render_template('My Account.html', events=events)

@main_bp.route('/save-event-changes/<int:event_id>', methods=['POST'])
def save_event_changes(event_id):
    # Retrieve the event by ID
    event = Event.query.get_or_404(event_id)
    
    # Update event fields with form data
    event.name = request.form.get('name', event.name)  # Keep existing value if not provided
    event.description = request.form.get('description', event.description)
    event.genre = request.form.get('genre', event.genre)
    event.location = request.form.get('location', event.location)
    event.time = request.form.get('time', event.time)
    event.contact_number = request.form.get('contact_number', event.contact_number)
    event.street_address = request.form.get('street_address', event.street_address)
    event.total_tickets = int(request.form.get('total_tickets', event.total_tickets))
    event.sold_tickets = int(request.form.get('sold_tickets', event.sold_tickets))
    
    # You can add other fields here as necessary

    # Save changes to the database
    db.session.commit()

    # Redirect back to the 'My Account' page (or any page you prefer)
    flash('Event changes saved successfully!', 'success')
    return redirect(url_for('main.my_account'))


@main_bp.route('/login', methods = (["GET", "POST"]))
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password_hash")

        if not name or not password:
            flash("Please enter both username and password.", "error")
            return render_template("Login Page.htm")

        user = User.query.filter_by(name=name).first()

        if user is None:
            flash("No account found with that username.", "error")
            return render_template("Login Page.html")

        if not check_password_hash(user.password_hash, password):
            flash("Incorrect password. Please try again.", "error")
            return render_template("Login Page.html")

        login_user(user)
        flash("Login successful!", "success")

        next_page = request.args.get("next")
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("main.index")
        
        return redirect(next_page)

        return render_template(login.html)
    return render_template('Login Page.html')

@main_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
            form.validate_on_submit()
            hashed_pass = generate_password_hash(form.password_hash.data)
            new_user = User(
                name=form.name.data,
                emailid=form.emailid.data,
                password_hash=hashed_pass,
                contact_number=form.contact_number.data,
                street_address=form.street_address.data
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))
    return render_template('Register Page.html')

@main_bp.route('/increment/<ticket_type>')
def increment(ticket_type):
    quantities = session.get('quantities', {})
    ticket_limits = {
        "standard-adult": None,
        "standard-concession": None,
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

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
