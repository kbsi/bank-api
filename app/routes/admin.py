from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.mongo import get_user_collection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """Lister tous les utilisateurs (Super Admin uniquement)."""
    users = list(get_user_collection().find({}, {"password_hash": 0}))
    return jsonify(users), 200

@admin_bp.route('/users/<user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    """Modifier un utilisateur (Admin uniquement)."""
    data = request.get_json()
    result = get_user_collection().update_one({"_id": user_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    return jsonify({"message": "Utilisateur mis à jour"}), 200

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Supprimer un utilisateur (Super Admin uniquement)."""
    result = get_user_collection().delete_one({"_id": user_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    return jsonify({"message": "Utilisateur supprimé"}), 200
