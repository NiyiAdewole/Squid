from dotenv import load_dotenv
import os
import redis
from flask import Flask, session
from flask_session import Session
from schemagenerator.app.web import web as web_blueprint

load_dotenv()

def create_app():
    app = Flask('__name__', 
                static_folder='schemagenerator/static', 
                template_folder='schemagenerator/templates')
    # app.config.update(
    #     TEMPLATES_AUTO_RELOAD=True
    # )
    
    app.secret_key = os.environ.get('SECRET_KEY')

    # Configure Redis for storing the session data on the server-side
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
    Session(app)

    # Import and register blueprints
    app.register_blueprint(web_blueprint)
    return app
