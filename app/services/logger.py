from app.services.mongo import get_log_collection
from datetime import datetime

def log_action(user_id, action_type, details=None):
    """Enregistrer une action dans les logs."""
    log_entry = {
        "user_id": user_id,
        "action_type": action_type,
        "details": details or {},
        "timestamp": datetime.utcnow()
    }
    get_log_collection().insert_one(log_entry)
