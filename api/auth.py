from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    if username is None:
        return jsonify({'message': 'Username is required'}), 400

    if User.check_email_exists(email=email):
        return jsonify({'message': 'Email already exists'}), 409

    user = User.get_user_by_username(username=username)

    if user is None:
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)

        user.save_to_database()
        return jsonify({'message': 'User created'}), 201

    return jsonify({'message': 'User with that username already exist'}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
        return jsonify({'error': 'Username/Password required'}), 400

    user = User.get_user_by_username(username=username)

    if not (user and user.check_password(password)):
        return jsonify({'error': 'Invalid username or password'}), 400

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token
        }), 200
