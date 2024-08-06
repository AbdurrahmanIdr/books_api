from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required, get_jwt,
                                current_user
                                )
from models.user import User
from models.token import TokenBlocklist

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


@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({
        'message': f'Welcome {current_user.username}',
        'user details': current_user.to_dict()
    }), 200


@auth_bp.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt().get('sub')
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token})


@auth_bp.get('/logout')
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()['jti']
    token_type = get_jwt()['type']
    token_b = TokenBlocklist(jti=jti)
    token_b.save()
    return jsonify({'message': f'{token_type} has been revoked successfully'}), 200
