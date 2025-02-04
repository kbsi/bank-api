from datetime import datetime
from bson.objectid import ObjectId

def create_transaction(from_account, to_account, amount, transaction_type="transfer", status="pending"):
    """Créer une transaction entre deux comptes."""
    return {
        "_id": str(ObjectId()),
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "type": transaction_type,  # transfer, deposit, withdrawal
        "timestamp": datetime.utcnow(),
        "status": status  # pending, completed, failed
    }

def complete_transaction(transaction):
    """Marque une transaction comme terminée."""
    transaction["status"] = "completed"
    transaction["timestamp"] = datetime.utcnow()
    return transaction

def fail_transaction(transaction):
    """Marque une transaction comme échouée."""
    transaction["status"] = "failed"
    transaction["timestamp"] = datetime.utcnow()
    return transaction
