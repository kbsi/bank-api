from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.mongo import get_log_collection

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    skip = (page - 1) * limit

    logs = list(get_log_collection().find().sort(
        'timestamp', -1).skip(skip).limit(limit))
    total_logs = get_log_collection().count_documents({})

    return jsonify({
        'logs': logs,
        'totalPages': (total_logs + limit - 1) // limit
    }), 200
