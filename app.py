from dotenv import load_dotenv
from flask import Flask, jsonify
from extensions import db, migrate, jwt
from secrets import token_urlsafe
from models.user import User
from models.token import TokenBlocklist
from api.books import books_bp
from api.auth import auth_bp
from api.users import users_bp


def create_app():
    """
    initialize the Flask instance
    """
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    app.config.from_prefixed_env()
    app.config['SECRET_KEY'] = token_urlsafe(32)
    s_key = token_urlsafe(32)
    app.config['JWT_SECRET_KEY'] = s_key
    print(s_key)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    # jwt user lookup
    @jwt.user_lookup_loader
    def user_loader_callback(jwt_identity, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username=identity).one_or_none()

    # jwt additional claim
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 'salimbey':
            return {
                "is_staff": True
            }
        return {
            "is_staff": False
        }

    # jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            "message": "Token expired",
            "expired": True
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Signature verification failed",
            "error": "Token is invalid"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Request does not contain valid token",
            "error": "Unauthorized"
        }), 401

    # jwt token blocklist
    @jwt.token_in_blocklist_loader
    def token_in_black_list_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
        return token is not None

    return app


if __name__ == "__main__":
    create_app().run()
