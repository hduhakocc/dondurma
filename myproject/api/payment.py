from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Payment, Order
from .utils import role_required
from datetime import datetime

payment_api = Blueprint('payment_api', __name__)

# Ödeme kaydı (üye ve admin)
@payment_api.route('/', methods=['POST'])
@jwt_required()
def add_payment():
    data = request.json
    order = Order.query.get(data['order_id'])
    if not order:
        return jsonify({'msg': 'Sipariş bulunamadı'}), 404
    payment = Payment(
        order_id=order.id,
        amount=data['amount'],
        payment_method=data.get('payment_method', 'cash'),
        payment_date=datetime.utcnow(),
        qr_code=data.get('qr_code')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'msg': 'Ödeme kaydedildi', 'id': payment.id}), 201

# Ödeme listeleme (admin ve üye)
@payment_api.route('/', methods=['GET'])
@jwt_required()
def list_payments():
    order_id = request.args.get('order_id')
    query = Payment.query
    if order_id:
        query = query.filter_by(order_id=order_id)
    payments = query.all()
    return jsonify([
        {'id': p.id, 'order_id': p.order_id, 'amount': p.amount, 'payment_method': p.payment_method, 'payment_date': p.payment_date, 'qr_code': p.qr_code}
        for p in payments
    ])
