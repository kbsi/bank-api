from flask_jwt_extended import create_access_token, create_refresh_token

def generate_tokens(user):
    """Générer des tokens JWT pour un utilisateur."""
    access_token = create_access_token(identity={"id": str(user["_id"]), "roles": user["roles"]})
    refresh_token = create_refresh_token(identity={"id": str(user["_id"]), "roles": user["roles"]})
    return access_token, refresh_token
