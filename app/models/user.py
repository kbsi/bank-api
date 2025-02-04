from bson.objectid import ObjectId

def create_user(email, password_hash, roles):
    return {
        "_id": str(ObjectId()),
        "email": email,
        "password_hash": password_hash,
        "roles": roles,
        "accounts": [],
        "created_at": datetime.utcnow()
    }
