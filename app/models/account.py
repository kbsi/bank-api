from datetime import datetime
from bson.objectid import ObjectId


def create_account(user_id, account_number, balance, currency="EUR"):
    """Créer un compte bancaire."""
    return {
        "_id": str(ObjectId()),
        "user_id": user_id,
        "account_number": account_number,
        "balance": balance,
        "currency": currency,
        "status": "active",
        "created_at": datetime.utcnow()
    }


def update_balance(account, amount):
    """Met à jour le solde d'un compte."""
    account["balance"] += amount
    return account


def deactivate_account(account):
    """Désactive un compte bancaire."""
    account["status"] = "inactive"
    return account
