from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Order, Customer
from .utils import role_required

delivery_api = Blueprint('delivery_api', __name__)

# Otomatik rota oluşturma
@delivery_api.route('/route', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_route():
    data = request.json
    order_ids = data.get('order_ids', [])
    
    if not order_ids:
        return jsonify({'msg': 'Sipariş ID\'leri gerekli'}), 400
        
    # Siparişleri ve müşteri adreslerini al
    orders = Order.query.filter(Order.id.in_(order_ids)).all()
    if not orders:
        return jsonify({'msg': 'Geçerli sipariş bulunamadı'}), 404
        
    # Teslimat rotası için adresleri hazırla
    delivery_points = []
    for order in orders:
        customer = Customer.query.get(order.customer_id)
        if customer and customer.address:
            delivery_points.append({
                'order_id': order.id,
                'address': customer.address,
                'customer_name': f"{customer.name} {customer.surname}",
                'phone': customer.phone
            })
    
    return jsonify({
        'msg': 'Teslimat rotası oluşturuldu',
        'delivery_points': delivery_points
    }), 200

# Teslimat durumu güncelleme
@delivery_api.route('/status', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def update_status():
    data = request.json
    if 'order_id' not in data or 'status' not in data:
        return jsonify({'msg': 'Sipariş ID ve durum gerekli'}), 400
        
    order = Order.query.get(data['order_id'])
    if not order:
        return jsonify({'msg': 'Sipariş bulunamadı'}), 404
        
    valid_statuses = ['pending', 'preparing', 'on_delivery', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'msg': 'Geçersiz durum'}), 400
        
    order.status = data['status']
    db.session.commit()
    
    return jsonify({
        'msg': 'Teslimat durumu güncellendi',
        'order_id': order.id,
        'status': order.status
    }), 200

# Teslimat listesi
@delivery_api.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_deliveries():
    status = request.args.get('status')
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.all()
    return jsonify([{
        'id': o.id,
        'customer_id': o.customer_id,
        'total': o.total,
        'status': o.status,
        'created_at': o.created_at
    } for o in orders]), 200
