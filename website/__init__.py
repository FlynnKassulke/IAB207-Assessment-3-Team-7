# __init__.py
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
    app.secret_key = 'somesecretkey'

    # Local import to avoid circular import issues
    from .models import db, Event, User
    db.init_app(app)

    with app.app_context():
        db.create_all()

        if not Event.query.first():
            sample_events = [
                Event(
                    name="Summer Vibes Festival",
                    description="Get ready for a vibrant beachside festival with top DJs and live bands!",
                    genre="Music",
                    photo="/img/summervibesfestthumbnail.png",
                    status="Sold Out",
                    location="Bondi Beach, Sydney, NSW",
                    time=datetime(2024, 7, 22),
                    contact_number=123456789,
                    street_address="Bondi Beach"
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
                    street_address="Thebarton Theatre"
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
                    street_address="Riverstage"
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
                    street_address="Brisbane Showgrounds"
                ),
                Event(
                    name="Jazz Fest 2024",
                    description="Smooth jazz and soulful performances at the annual Jazz Fest.",
                    genre="Jazz",
                    photo="/img/bluesbrewsthumbnail.png",
                    status="Open",
                    location="Melbourne Convention Centre, Melbourne, VIC",
                    time=datetime(2024, 10, 15),
                    contact_number=223344556,
                    street_address="Melbourne Convention Centre"
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
                    street_address="Coffs Harbour"
                )
            ]
            db.session.bulk_save_objects(sample_events)
            db.session.commit()

    Bootstrap5(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)

    # Register blueprints after app is created
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
