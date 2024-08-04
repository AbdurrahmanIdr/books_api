from flask import Blueprint, jsonify, request
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username', None)
    if username is None:
        return jsonify({'message': 'Username is required'}), 400

    user = User.get_user_by_username(username=username)
    if user is None:
        email = data.get('email', None)
        password = data.get('password', None)

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)

        user.save_to_database()
        return jsonify({'message': 'User created'}), 201

    return jsonify({'message': 'User with that username already exist'}), 409
