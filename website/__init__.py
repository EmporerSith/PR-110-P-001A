from flask import Flask
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'zqwerty'

    app.config['SESSION_TYPE'] = 'filesystem'  # You can also use 'redis' or 'mongodb' for more advanced options
    app.config['SESSION_PERMANENT'] = False  # Optional: Set session permanence (default is False)
    
    # Initialize Flask-Session
    Session(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app