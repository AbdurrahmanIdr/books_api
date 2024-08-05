from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.user import User
from models.schemas import UserSchema

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 3, type=int)
    )

    results = UserSchema().dump(users, many=True)

    return jsonify({
        'status': 'success',
        'users': results
    }), 200
