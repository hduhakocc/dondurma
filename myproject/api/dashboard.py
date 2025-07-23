from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Order, Product, Payment
from sqlalchemy import func

dashboard_api = Blueprint('dashboard_api', __name__)

# Dashboard verileri (sipariş sayısı, ciro, teslimat durumu, stok uyarıları)
@dashboard_api.route('/', methods=['GET'])
@jwt_required()
def dashboard():
    order_count = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total)).scalar() or 0
    delivered_count = Order.query.filter_by(status='delivered').count()
    pending_count = Order.query.filter_by(status='pending').count()
    low_stock = Product.query.filter(Product.stock < 10).all()
    low_stock_list = [{'id': p.id, 'name': p.name, 'stock': p.stock} for p in low_stock]
    return jsonify({
        'order_count': order_count,
        'total_revenue': total_revenue,
        'delivered_count': delivered_count,
        'pending_count': pending_count,
        'low_stock': low_stock_list
    })
