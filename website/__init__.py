from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from datetime import datetime

def create_app():
    # Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
    app.secret_key = 'somesecretkey'

    # Initialize extensions
    Bootstrap5(app)

    # Import and initialize database
    from .models import db, Event, User
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Populate sample data if no events exist
        if not Event.query.first():
            sample_events = [
                Event(
                    name="Summer Vibes Festival",
                    description="Get ready for a vibrant beachside festival with top DJs and live bands!",
                    genre="Music",
                    photo="/img/summervibesfestthumbnail.png",
                    status="Sold Out",
                    location="Bondi Beach, Sydney, NSW",
                    time=datetime(2024, 12, 22),
                    contact_number=123456789,
                    street_address="Bondi Beach",
                    total_tickets=200,
                    sold_tickets=200,
                    userid=100
                ),
                Event(
                    name="Rock Revolution 2024",
                    description="Electrifying performances from legendary rock bands, live on stage!",
                    genre="Rock",
                    photo="/img/rockrevolutionthumbnail.png",
                    status="Inactive",
                    location="Thebarton Theatre, Adelaide, SA",
                    time=datetime(2024, 9, 14),
                    contact_number=987654321,
                    street_address="Thebarton Theatre",
                    total_tickets=200,
                    sold_tickets=200,
                    userid=100
                ),
                Event(
                    name="Flume Live in Concert",
                    description="An unforgettable night with Flume and his cutting-edge beats.",
                    genre="Electronic",
                    photo="/img/flumethumbnail.png",
                    status="Open",
                    location="Riverstage, Brisbane, QLD",
                    time=datetime(2024, 10, 8),
                    contact_number=112233445,
                    street_address="Riverstage",
                    total_tickets=200,
                    sold_tickets=200,
                    userid=100
                ),
                Event(
                    name="Electric Pulse Festival",
                    description="Experience 3 days of electronic music and mesmerizing visuals.",
                    genre="Electronic",
                    photo="/img/electricpulsethumbnail.png",
                    status="Cancelled",
                    location="Brisbane Showgrounds, Brisbane, QLD",
                    time=datetime(2024, 8, 17),
                    contact_number=556677889,
                    street_address="Brisbane Showgrounds",
                    total_tickets=200,
                    sold_tickets=200,
                    userid=100
                ),
                Event(
                    name="Jazz Fest 2024",
                    description="Smooth jazz and soulful performances at the annual Jazz Fest.",
                    genre="Jazz",
                    photo="/img/bluesbrewsthumbnail.png",
                    status="Open",
                    location="Melbourne Convention Centre, Melbourne, VIC",
                    time=datetime(2025, 10, 15),
                    contact_number=223344556,
                    street_address="Melbourne Convention Centre",
                    total_tickets=200,
                    sold_tickets=200,
                    userid=100
                ),
                Event(
                    name="Country Fest",
                    description="A weekend of live performances from top country artists.",
                    genre="Country",
                    photo="/img/folkinthewoodsthumbnail.png",
                    status="Sold Out",
                    location="Coffs Harbour, NSW",
                    time=datetime(2024, 11, 5),
                    contact_number=334455667,
                    street_address="Coffs Harbour",
                    total_tickets=200,
                    sold_tickets=200,
                    userid=100
                )
            ]
            db.session.bulk_save_objects(sample_events)
            db.session.commit()

    # Configure and initialize LoginManager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'  # Assumes an 'auth' blueprint with a 'login' route

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)

    # Register blueprints
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
