from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Log, User
from .utils import role_required
from datetime import datetime, timedelta

logs_api = Blueprint('logs_api', __name__)

# Logları listele (sadece admin)
@logs_api.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_logs():
    # Filtreler
    days = request.args.get('days', 7, type=int)
    action = request.args.get('action')
    user_id = request.args.get('user_id', type=int)
    limit = request.args.get('limit', 100, type=int)
    
    since_date = datetime.utcnow() - timedelta(days=days)
    query = Log.query.filter(Log.created_at >= since_date)
    
    if action:
        query = query.filter_by(action=action)
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    logs = query.order_by(Log.created_at.desc()).limit(limit).all()
    
    # Log kayıtlarını kullanıcı bilgileriyle birleştir
    result = []
    for log in logs:
        user = User.query.get(log.user_id)
        log_data = {
            'id': log.id,
            'user_id': log.user_id,
            'username': user.username if user else 'Unknown',
            'action': log.action,
            'details': log.details,
            'created_at': log.created_at
        }
        result.append(log_data)
    
    return jsonify(result)

@logs_api.route('/actions', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_actions():
    # Mevcut log tiplerini listele
    actions = db.session.query(Log.action).distinct().all()
    return jsonify([action[0] for action in actions])

@logs_api.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_stats():
    days = request.args.get('days', 7, type=int)
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Aksiyon bazlı istatistikler
    action_stats = db.session.query(
        Log.action,
        db.func.count(Log.id)
    ).filter(Log.created_at >= since_date).group_by(Log.action).all()
    
    # Kullanıcı bazlı istatistikler
    user_stats = db.session.query(
        User.username,
        db.func.count(Log.id)
    ).join(Log).filter(Log.created_at >= since_date).group_by(User.username).all()
    
    return jsonify({
        'action_stats': dict(action_stats),
        'user_stats': dict(user_stats)
    })
