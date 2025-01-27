
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

login_manager = LoginManager()
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "gadjahmada24TRI"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .views import views
    from .auth import auth
    from .moodtrack import mood
    from .models import User
    from .audioplay import  audioplay

    app.register_blueprint(audioplay, url_prefix =  "/")
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(mood, url_prefix = "/")

    db.init_app(app)
    with app.app_context():
        create_database(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_database(app):
    if not path.exists(DB_NAME):
        print("Database tidak ada, membuat database...")
        with app.app_context():
            db.create_all()
    else:
        print("Database sudah ada.")

