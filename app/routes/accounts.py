from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import create_account, update_balance, deactivate_account
from app.models.transaction import create_transaction, complete_transaction, fail_transaction

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/create', methods=['POST'])
@jwt_required()
def create_new_account():
    """Créer un nouveau compte bancaire."""
    user_identity = get_jwt_identity()
    data = request.get_json()
    
    # Validation des données (simplifiée)
    if not data.get("balance") or not data.get("currency"):
        return jsonify({"error": "Les champs 'balance' et 'currency' sont requis"}), 400
    
    new_account = create_account(
        user_id=user_identity["_id"],
        account_number=f"FR{user_identity['_id'][-6:]}{data['balance']}",
        balance=data["balance"],
        currency=data["currency"]
    )
    
    # Sauvegarde dans MongoDB (exemple)
    from app.services.mongo import get_account_collection
    get_account_collection().insert_one(new_account)
    
    return jsonify(new_account), 201

@accounts_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer_money():
    """Effectuer un transfert entre deux comptes."""
    data = request.get_json()
    
    # Validation des données (simplifiée)
    if not data.get("from_account") or not data.get("to_account") or not data.get("amount"):
        return jsonify({"error": "Les champs 'from_account', 'to_account' et 'amount' sont requis"}), 400
    
    from app.services.mongo import get_account_collection, get_transaction_collection
    
    from_acc = get_account_collection().find_one({"_id": data["from_account"]})
    to_acc = get_account_collection().find_one({"_id": data["to_account"]})
    
    if not from_acc or not to_acc:
        return jsonify({"error": "L'un des comptes n'existe pas"}), 404
    
    if from_acc["balance"] < data["amount"]:
        return jsonify({"error": "Solde insuffisant"}), 400
    
    # Création de la transaction et mise à jour des soldes des comptes.
    transaction = create_transaction(data["from_account"], data["to_account"], data["amount"])
    
    try:
        update_balance(from_acc, -data["amount"])
        update_balance(to_acc, data["amount"])
        
        complete_transaction(transaction)
        
        # Sauvegarde dans MongoDB (exemple)
        get_transaction_collection().insert_one(transaction)
        get_account_collection().update_one({"_id": from_acc["_id"]}, {"$set": from_acc})
        get_account_collection().update_one({"_id": to_acc["_id"]}, {"$set": to_acc})
        
        return jsonify(transaction), 200
    
    except Exception as e:
        fail_transaction(transaction)
        return jsonify({"error": str(e)}), 500

@accounts_bp.route('/<account_id>/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_user_account(account_id):
    """Désactiver un compte bancaire."""
    from app.services.mongo import get_account_collection
    
    account = get_account_collection().find_one({"_id": account_id})
    
    if not account:
        return jsonify({"error": "Compte introuvable"}), 404
    
    updated_account = deactivate_account(account)
    
    # Sauvegarde dans MongoDB (exemple)
    get_account_collection().update_one({"_id": account["_id"]}, {"$set": updated_account})
    
    return jsonify(updated_account), 200
