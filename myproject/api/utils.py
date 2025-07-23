from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

# Rol tabanlı yetkilendirme decorator'ı
def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if identity and identity.get('role') in roles:
                return fn(*args, **kwargs)
            return jsonify({'msg': 'Yetkisiz erişim'}), 403
        return wrapper
    return decorator
