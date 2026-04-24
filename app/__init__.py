from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():

    # ✅ Enable instance folder
    app = Flask(__name__, instance_relative_config=True)

    # ✅ Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # ✅ Database path inside instance folder
    db_path = os.path.join(app.instance_path, "pigpeople.db")

    # CONFIG
    app.config["SECRET_KEY"] = "pigpeople_secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # INIT EXTENSIONS
    db.init_app(app)

    login_manager.login_view = "main.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # REGISTER ROUTES
    from .routes import main
    app.register_blueprint(main)

    # 🧠 CREATE DB + DEFAULT ADMIN
    with app.app_context():
        db.create_all()

        from werkzeug.security import generate_password_hash

        existing_admin = User.query.filter_by(username="masuwa_chikonkolo").first()

        if not existing_admin:
            admin = User(
                name="Masuwa Chikonkolo",
                username="masuwa_chikonkolo",
                password=generate_password_hash("chikonkz999"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created!")

    return app