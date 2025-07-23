from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .utils import role_required

# NOT: Gerçek WhatsApp Business API entegrasyonu için ek geliştirme gerekir.
auto_message_api = Blueprint('auto_message_api', __name__)

@auto_message_api.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    data = request.json
    # Burada WhatsApp Business API ile mesaj gönderme işlemi yapılabilir
    # Örnek: data['phone'], data['message']
    return jsonify({'msg': 'Otomatik mesaj entegrasyonu için hazır', 'to': data.get('phone')}), 200
