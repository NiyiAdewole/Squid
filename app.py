from dotenv import load_dotenv
import os
from flask import Flask
from schemagenerator.app.web import web as web_blueprint

load_dotenv()

def create_app():
    app = Flask('__name__', 
                static_folder='schemagenerator/static', 
                template_folder='schemagenerator/templates')
    
    app.secret_key = os.environ.get('SECRET_KEY')
    # Import and register blueprints
    app.register_blueprint(web_blueprint)
    return app
