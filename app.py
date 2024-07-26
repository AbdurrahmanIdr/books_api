from flask import Flask
from extensions import db
from books import books_bp
from dotenv import load_dotenv


def create_app():
    """
    initialize the Flask instance
    """
    app = Flask(__name__)    
    
    # Load environment variables from .env file
    load_dotenv()
    
    app.config.from_prefixed_env()

    # initialize extensions
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    # register blueprints
    app.register_blueprint(books_bp, url_prefix='/books')

    return app


if __name__ == "__main__":
    create_app().run()
