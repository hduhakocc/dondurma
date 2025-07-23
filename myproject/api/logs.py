from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Log, User
from .utils import role_required

logs_api = Blueprint('logs_api', __name__)

# Logları listele (sadece admin)
@logs_api.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_logs():
    logs = Log.query.order_by(Log.created_at.desc()).limit(100).all()
    return jsonify([
        {'id': l.id, 'user_id': l.user_id, 'action': l.action, 'details': l.details, 'created_at': l.created_at}
        for l in logs
    ])
