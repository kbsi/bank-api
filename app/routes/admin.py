from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.mongo import get_user_collection
import logging

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


def check_user_role(required_role):
    current_user = get_jwt_identity()
    logger.debug(f"Identité actuelle : {current_user}")
    user = get_user_collection().find_one({"email": current_user})
    if user is None or required_role not in user["roles"]:
        return False
    return True


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'responses': {
        200: {
            'description': 'Liste de tous les utilisateurs',
            'examples': {
                'application/json': [
                    {
                        '_id': 'user_id',
                        'username': 'user1',
                        'email': 'user1@example.com'
                    },
                    {
                        '_id': 'user_id2',
                        'username': 'user2',
                        'email': 'user2@example.com'
                    }
                ]
            }
        }
    }
})
def list_users():
    """Lister tous les utilisateurs (Admin uniquement)."""
    logger.debug("Début de la fonction list_users")
    if not check_user_role("admin"):
        logger.debug("Accès refusé : l'utilisateur n'a pas le rôle admin")
        return jsonify({"message": "Access forbidden"}), 403
    try:
        users = list(get_user_collection().find({}, {"password_hash": 0}))
        return jsonify(users), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des utilisateurs : {e}")
        return jsonify({"message": "Erreur lors de la récupération des utilisateurs"}), 500


@admin_bp.route('/users/<user_id>', methods=['PATCH'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID de l\'utilisateur à modifier'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Utilisateur mis à jour',
            'examples': {
                'application/json': {
                    'message': 'Utilisateur mis à jour'
                }
            }
        },
        404: {
            'description': 'Utilisateur non trouvé',
            'examples': {
                'application/json': {
                    'message': 'Utilisateur non trouvé'
                }
            }
        }
    }
})
def update_user(user_id):
    """Modifier un utilisateur (Admin uniquement)."""
    if not check_user_role("admin"):
        return jsonify({"message": "Access forbidden"}), 403

    data = request.get_json()
    result = get_user_collection().update_one({"_id": user_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    return jsonify({"message": "Utilisateur mis à jour"}), 200


@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID de l\'utilisateur à supprimer'
        }
    ],
    'responses': {
        200: {
            'description': 'Utilisateur supprimé',
            'examples': {
                'application/json': {
                    'message': 'Utilisateur supprimé'
                }
            }
        },
        404: {
            'description': 'Utilisateur non trouvé',
            'examples': {
                'application/json': {
                    'message': 'Utilisateur non trouvé'
                }
            }
        }
    }
})
def delete_user(user_id):
    """Supprimer un utilisateur (Admin uniquement)."""
    if not check_user_role("admin"):
        return jsonify({"message": "Access forbidden"}), 403

    result = get_user_collection().delete_one({"_id": user_id})
    if result.deleted_count == 0:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    return jsonify({"message": "Utilisateur supprimé"}), 200
