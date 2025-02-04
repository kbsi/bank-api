from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    password_hash = generate_password_hash(data['password'])
    # Enregistrement dans MongoDB ici...
    return jsonify(message="Utilisateur enregistré avec succès"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Vérification des identifiants ici...
    token = create_access_token(identity={"email": data['email'], "roles": ["client"]})
    return jsonify(access_token=token), 200
