from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.models.account import create_account, update_balance, deactivate_account
from app.models.transaction import create_transaction, complete_transaction, fail_transaction
from app.services.mongo import get_account_collection, get_transaction_collection, get_user_collection
from bson import ObjectId  # Ajoutez cette ligne pour importer ObjectId
import logging

accounts_bp = Blueprint('accounts', __name__)
logger = logging.getLogger(__name__)


def check_user_role(required_role):
    current_user = get_jwt_identity()
    user = get_user_collection().find_one({"email": current_user})
    if user is None or required_role not in user["roles"]:
        return False
    return True


@accounts_bp.route('/create', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Accounts'],
    'responses': {
        201: {
            'description': 'Compte créé avec succès',
            'examples': {
                'application/json': {
                    'user_id': 'user_id',
                    'account_number': 'FR1234567890',
                    'balance': 1000,
                    'currency': 'EUR'
                }
            }
        },
        400: {
            'description': 'Erreur de validation des données',
            'examples': {
                'application/json': {
                    'error': 'Les champs \'balance\' et \'currency\' sont requis'
                }
            }
        }
    }
})
def create_new_account():
    """Créer un nouveau compte bancaire."""
    user_identity = get_jwt_identity()
    data = request.get_json()

    # Validation des données (simplifiée)
    if not data.get("balance") or not data.get("currency"):
        return jsonify({"error": "Les champs 'balance' et 'currency' sont requis"}), 400

    new_account = create_account(
        user_id=user_identity,
        account_number=f"FR{user_identity[-6:]}{data['balance']}",
        balance=data["balance"],
        currency=data["currency"]
    )

    # Sauvegarde dans MongoDB
    get_account_collection().insert_one(new_account)

    return jsonify(new_account), 201


@accounts_bp.route('/transfer', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Accounts'],
    'responses': {
        200: {
            'description': 'Transfert effectué avec succès',
            'examples': {
                'application/json': {
                    'from_account': 'from_account_id',
                    'to_account': 'to_account_id',
                    'amount': 100
                }
            }
        },
        400: {
            'description': 'Erreur de validation des données',
            'examples': {
                'application/json': {
                    'error': 'Les champs \'from_account\', \'to_account\' et \'amount\' sont requis'
                }
            }
        },
        404: {
            'description': 'Compte introuvable',
            'examples': {
                'application/json': {
                    'error': 'L\'un des comptes n\'existe pas'
                }
            }
        }
    }
})
def transfer_money():
    """Effectuer un transfert entre deux comptes."""
    data = request.get_json()

    # Validation des données (simplifiée)
    if not data.get("from_account") or not data.get("to_account") or not data.get("amount"):
        return jsonify({"error": "Les champs 'from_account', 'to_account' et 'amount' sont requis"}), 400

    from_acc = get_account_collection().find_one(
        {"_id": ObjectId(data["from_account"])})
    to_acc = get_account_collection().find_one(
        {"_id": ObjectId(data["to_account"])})

    if not from_acc or not to_acc:
        return jsonify({"error": "L'un des comptes n'existe pas"}), 404

    if from_acc["balance"] < data["amount"]:
        return jsonify({"error": "Solde insuffisant"}), 400

    # Création de la transaction et mise à jour des soldes des comptes.
    transaction = create_transaction(
        data["from_account"], data["to_account"], data["amount"])

    try:
        update_balance(from_acc, -data["amount"])
        update_balance(to_acc, data["amount"])

        complete_transaction(transaction)

        # Sauvegarde dans MongoDB
        get_transaction_collection().insert_one(transaction)
        get_account_collection().update_one(
            {"_id": from_acc["_id"]}, {"$set": from_acc})
        get_account_collection().update_one(
            {"_id": to_acc["_id"]}, {"$set": to_acc})

        return jsonify(transaction), 200

    except Exception as e:
        fail_transaction(transaction)
        return jsonify({"error": str(e)}), 500


@accounts_bp.route('/<account_id>/deactivate', methods=['PATCH'])
@jwt_required()
@swag_from({
    'tags': ['Accounts'],
    'responses': {
        200: {
            'description': 'Compte désactivé avec succès',
            'examples': {
                'application/json': {
                    'account_id': 'account_id',
                    'status': 'deactivated'
                }
            }
        },
        404: {
            'description': 'Compte introuvable',
            'examples': {
                'application/json': {
                    'error': 'Compte introuvable'
                }
            }
        }
    }
})
def deactivate_user_account(account_id):
    """Désactiver un compte bancaire."""
    account = get_account_collection().find_one({"_id": ObjectId(account_id)})

    if not account:
        return jsonify({"error": "Compte introuvable"}), 404

    updated_account = deactivate_account(account)

    # Sauvegarde dans MongoDB
    get_account_collection().update_one(
        {"_id": account["_id"]}, {"$set": updated_account})

    return jsonify(updated_account), 200


@accounts_bp.route('/my-accounts', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Accounts'],
    'responses': {
        200: {
            'description': 'Liste des comptes de l\'utilisateur connecté',
            'examples': {
                'application/json': [
                    {
                        'user_id': 'user_id',
                        'account_number': 'FR1234567890',
                        'balance': 1000,
                        'currency': 'EUR'
                    },
                    {
                        'user_id': 'user_id',
                        'account_number': 'FR0987654321',
                        'balance': 2000,
                        'currency': 'USD'
                    }
                ]
            }
        },
        404: {
            'description': 'Aucun compte trouvé pour cet utilisateur',
            'examples': {
                'application/json': {
                    'error': 'Aucun compte trouvé pour cet utilisateur'
                }
            }
        }
    }
})
def get_user_accounts():
    """Récupérer la liste des comptes de l'utilisateur connecté."""
    user_identity = get_jwt_identity()
    user = get_user_collection().find_one({"email": user_identity})
    accounts = list(get_account_collection().find({"user_id": user["_id"]}))

    if not accounts:
        return jsonify({"error": "Aucun compte trouvé pour cet utilisateur"}), 404

    return jsonify(accounts), 200


@accounts_bp.route('/<account_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Accounts'],
    'parameters': [
        {
            'name': 'account_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID du compte'
        }
    ],
    'responses': {
        200: {
            'description': 'Détails du compte',
            'examples': {
                'application/json': {
                    'user_id': 'user_id',
                    'account_number': 'FR1234567890',
                    'balance': 1000,
                    'currency': 'EUR',
                    'status': 'active',
                    'created_at': '2025-02-18T11:11:47'
                }
            }
        },
        403: {
            'description': 'Accès refusé',
            'examples': {
                'application/json': {
                    'error': 'Accès refusé'
                }
            }
        },
        404: {
            'description': 'Compte introuvable',
            'examples': {
                'application/json': {
                    'error': 'Compte introuvable'
                }
            }
        }
    }
})
def get_account_details(account_id):

    logger.log(logging.DEBUG, f"account_id: {account_id}")

    """Récupérer les détails d'un compte."""
    user_identity = get_jwt_identity()
    account = get_account_collection().find_one({"_id": ObjectId(account_id)})

    if not account:
        return jsonify({"error": "Compte introuvable"}), 404

    # Vérifier si l'utilisateur est admin ou propriétaire du compte
    user = get_user_collection().find_one({"email": user_identity})
    if not check_user_role("admin") and account["user_id"] != user["_id"]:
        return jsonify({"error": "Accès refusé"}), 403

    return jsonify(account), 200


@accounts_bp.route('/<account_id>/transactions', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Accounts'],
    'parameters': [
        {
            'name': 'account_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID du compte'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Date de début pour les transactions'
        }
    ],
    'responses': {
        200: {
            'description': 'Liste des transactions du compte',
            'examples': {
                'application/json': [
                    {
                        'transaction_id': 'transaction_id',
                        'from_account': 'from_account_id',
                        'to_account': 'to_account_id',
                        'amount': 100,
                        'currency': 'EUR',
                        'timestamp': '2025-02-18T11:11:47'
                    },
                    {
                        'transaction_id': 'transaction_id2',
                        'from_account': 'from_account_id2',
                        'to_account': 'to_account_id2',
                        'amount': 200,
                        'currency': 'USD',
                        'timestamp': '2025-02-18T11:12:47'
                    }
                ]
            }
        },
        403: {
            'description': 'Accès refusé',
            'examples': {
                'application/json': {
                    'error': 'Accès refusé'
                }
            }
        },
        404: {
            'description': 'Compte ou transactions introuvables',
            'examples': {
                'application/json': {
                    'error': 'Compte ou transactions introuvables'
                }
            }
        }
    }
})
def get_account_transactions(account_id):
    """Récupérer la liste des transactions d'un compte."""
    user_identity = get_jwt_identity()
    account = get_account_collection().find_one({"_id": ObjectId(account_id)})

    if not account:
        return jsonify({"error": "Compte introuvable"}), 404

    logger.log(logging.DEBUG, f"account_number: {account['account_number']}")

    # Vérifier si l'utilisateur est admin ou propriétaire du compte
    user = get_user_collection().find_one({"email": user_identity})
    if not check_user_role("admin") and account["user_id"] != user["_id"]:
        return jsonify({"error": "Accès refusé"}), 403

    start_date = request.args.get('start_date')
    transactions = list(get_transaction_collection().find({
        "$or": [
            {"from_account": account["account_number"]},
            {"to_account": account["account_number"]}
        ]
    }))

    if not transactions:
        return jsonify({"error": "Aucune transaction trouvée pour ce compte"}), 404

    return jsonify(transactions), 200
