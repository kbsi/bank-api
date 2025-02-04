from flask import jsonify

def validate_user_data(data):
    required_fields = ["email", "password", "roles"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Le champ {field} est requis"}), 400
    return None

def validate_account_data(data):
    required_fields = ["balance", "currency"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Le champ {field} est requis"}), 400
    return None
