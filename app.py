from flask import Flask
from schemagenerator.app.web import web as web_blueprint

def create_app():
    app = Flask('__name__', 
                static_folder='schemagenerator/static', 
                template_folder='schemagenerator/templates')
    
    # Import and register blueprints
    app.register_blueprint(web_blueprint)
    return app
