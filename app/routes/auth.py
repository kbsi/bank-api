import logging
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.mongo import get_user_collection, mongo
from app.services.auth import generate_tokens

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'examples': {
                'application/json': {
                    'message': 'User registered successfully'
                }
            }
        }
    }
})
def register():
    data = request.get_json()
    password_hash = generate_password_hash(data['password'])
    # Enregistrement dans MongoDB ici...
    get_user_collection().insert_one({
        "email": data['email'],
        "password_hash": password_hash
    })
    return jsonify(message="User registered successfully"), 201


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'examples': {
                'application/json': {
                    'access_token': 'your_jwt_access_token',
                    'refresh_token': 'your_jwt_refresh_token'
                }
            }
        },
        401: {
            'description': 'Invalid credentials',
            'examples': {
                'application/json': {
                    'msg': 'Invalid email or password'
                }
            }
        }
    }
})
def login():
    data = request.get_json()
    user = get_user_collection().find_one({"email": data['email']})
    if user and check_password_hash(user['password_hash'], data['password']):
        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify(msg="Invalid email or password"), 401


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@swag_from({
    'tags': ['Authentication'],
    'responses': {
        200: {
            'description': 'Token refreshed successfully',
            'examples': {
                'application/json': {
                    'access_token': 'your_new_jwt_access_token'
                }
            }
        },
        401: {
            'description': 'Invalid refresh token',
            'examples': {
                'application/json': {
                    'msg': 'Invalid refresh token'
                }
            }
        }
    }
})
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Authentication'],
    'responses': {
        200: {
            'description': 'User information retrieved successfully',
            'examples': {
                'application/json': {
                    'email': 'user@example.com',
                    'firstName': 'John',
                    'lastName': 'Doe'
                }
            }
        },
        401: {
            'description': 'Invalid token',
            'examples': {
                'application/json': {
                    'msg': 'Invalid token'
                }
            }
        }
    }
})
def get_user_info():
    current_user_email = get_jwt_identity()
    user = get_user_collection().find_one(
        {"email": current_user_email}, {"_id": 0, "password_hash": 0})
    if user:
        return jsonify(user), 200
    return jsonify(msg="User not found"), 404
