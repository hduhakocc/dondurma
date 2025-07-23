from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Order
from .utils import role_required

# Dağıtım işlemleri için blueprint
delivery_api = Blueprint('delivery_api', __name__)

# Otomatik rota oluşturma (örnek, Google Maps API entegrasyonu için hazır)
@delivery_api.route('/route', methods=['POST'])
@jwt_required()
def create_route():
    data = request.json
    # Burada Google Maps API ile rota oluşturma işlemi yapılabilir
    # Örnek: data['order_ids'] ile seçili siparişlerin adreslerinden rota oluşturulacak
    return jsonify({'msg': 'Rota oluşturma entegrasyonu için hazır', 'orders': data.get('order_ids', [])}), 200

# Teslimat durumu güncelleme
@delivery_api.route('/status', methods=['POST'])
@jwt_required()
def update_status():
    data = request.json
    order = Order.query.get(data['order_id'])
    if not order:
        return jsonify({'msg': 'Sipariş bulunamadı'}), 404
    order.status = data.get('status', 'delivered')
    db.session.commit()
    return jsonify({'msg': 'Teslimat durumu güncellendi', 'order_id': order.id, 'status': order.status}), 200
