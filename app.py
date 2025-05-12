from dotenv import load_dotenv
import os
import redis
import subprocess
from flask import Flask, session
from flask_session import Session
from schemagenerator.app.models import db
from schemagenerator.app.web import web as web_blueprint

load_dotenv()

def start_redis_server():
    """Start the Redis server if it's not already running."""
    try:
        # Check if Redis is already running
        redis_client = redis.StrictRedis(host='127.0.0.1', port=6379)
        redis_client.ping()
        print("Redis server is already running.")
    except redis.exceptions.ConnectionError:
        # Start Redis server
        print("Starting Redis server...")
        subprocess.Popen(["redis-server"])
        print("Redis server started.")

def create_app():
    app = Flask('__name__', 
                static_folder='schemagenerator/static', 
                template_folder='schemagenerator/templates')
    
    app.secret_key = os.environ.get('SECRET_KEY')

    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize the database with the app

    # Configure Redis for storing the session data on the server-side
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
    Session(app)

    # Only start Redis server in development mode
    if os.environ.get('FLASK_ENV') == 'development':
        start_redis_server()

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Import and register blueprints
    app.register_blueprint(web_blueprint)
    return app
