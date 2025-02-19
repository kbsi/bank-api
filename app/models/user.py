from bson.objectid import ObjectId


def create_user(email, password_hash, roles, address, first_name, last_name):
    return {
        "_id": str(ObjectId()),
        "email": email,
        "password_hash": password_hash,
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "roles": roles,
        "created_at": datetime.utcnow()
    }
