from dotenv import load_dotenv
from flask import Flask
from extensions import db, migrate
from secrets import token_urlsafe
from api.books import books_bp
from api.auth import auth_bp


def create_app():
    """
    initialize the Flask instance
    """
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    app.config.from_prefixed_env()
    app.config['SECRET_KEY'] = token_urlsafe(32)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
