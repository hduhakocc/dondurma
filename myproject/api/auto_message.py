from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .utils import role_required
from .models import db, Customer, Order
from datetime import datetime

auto_message_api = Blueprint('auto_message_api', __name__)

@auto_message_api.route('/send', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def send_message():
    data = request.json
    
    if not data.get('phone') or not data.get('message'):
        return jsonify({'msg': 'Telefon numarası ve mesaj gerekli'}), 400
    
    # Mesaj şablonlarını kontrol et
    template = data.get('template')
    if template:
        message = create_message_from_template(template, data.get('params', {}))
    else:
        message = data.get('message')
    
    # Mesaj gönderme simülasyonu
    result = {
        'success': True,
        'to': data['phone'],
        'message': message,
        'sent_at': datetime.utcnow().isoformat()
    }
    
    return jsonify(result), 200

@auto_message_api.route('/templates', methods=['GET'])
@jwt_required()
def list_templates():
    templates = [
        {
            'id': 'order_confirmation',
            'name': 'Sipariş Onayı',
            'template': 'Sayın {customer_name}, {order_id} numaralı siparişiniz alınmıştır. Toplam tutar: ₺{total}'
        },
        {
            'id': 'delivery_status',
            'name': 'Teslimat Durumu',
            'template': 'Sayın {customer_name}, siparişiniz {status} durumundadır.'
        },
        {
            'id': 'payment_reminder',
            'name': 'Ödeme Hatırlatma',
            'template': 'Sayın {customer_name}, {order_id} numaralı siparişinizin ₺{amount} tutarındaki ödemesi beklenmektedir.'
        }
    ]
    return jsonify(templates)

@auto_message_api.route('/bulk-send', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def bulk_send():
    data = request.json
    template_id = data.get('template_id')
    filter_status = data.get('filter_status')
    
    if not template_id:
        return jsonify({'msg': 'Şablon ID\'si gerekli'}), 400
    
    # Filtreye göre müşterileri bul
    query = Order.query
    if filter_status:
        query = query.filter_by(status=filter_status)
    
    orders = query.all()
    results = []
    
    for order in orders:
        customer = Customer.query.get(order.customer_id)
        if customer and customer.phone:
            message = create_message_from_template(template_id, {
                'customer_name': f"{customer.name} {customer.surname}",
                'order_id': order.id,
                'total': order.total,
                'status': order.status
            })
            
            # Mesaj gönderme simülasyonu
            results.append({
                'success': True,
                'to': customer.phone,
                'message': message
            })
    
    return jsonify({
        'total_sent': len(results),
        'results': results
    })

def create_message_from_template(template_id, params):
    templates = {
        'order_confirmation': 'Sayın {customer_name}, {order_id} numaralı siparişiniz alınmıştır. Toplam tutar: ₺{total}',
        'delivery_status': 'Sayın {customer_name}, siparişiniz {status} durumundadır.',
        'payment_reminder': 'Sayın {customer_name}, {order_id} numaralı siparişinizin ₺{amount} tutarındaki ödemesi beklenmektedir.'
    }
    
    template = templates.get(template_id)
    if not template:
        return None
        
    try:
        return template.format(**params)
    except KeyError:
        return None
