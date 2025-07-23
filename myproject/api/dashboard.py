from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Order, Product, Payment, Customer
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_api = Blueprint('dashboard_api', __name__)

# Dashboard verileri
@dashboard_api.route('/', methods=['GET'])
@jwt_required()
def dashboard():
    user = get_jwt_identity()
    is_admin = user.get('role') == 'admin'
    
    # Tarih filtresi
    days = request.args.get('days', 30, type=int)
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Temel sorgular
    query = Order.query.filter(Order.created_at >= since_date)
    if not is_admin:
        query = query.filter_by(user_id=user.get('id'))
    
    # Sipariş istatistikleri
    order_count = query.count()
    total_revenue = db.session.query(func.sum(Order.total)).filter(Order.created_at >= since_date).scalar() or 0
    
    # Durum bazlı sayılar
    status_counts = {
        'pending': query.filter_by(status='pending').count(),
        'preparing': query.filter_by(status='preparing').count(),
        'on_delivery': query.filter_by(status='on_delivery').count(),
        'delivered': query.filter_by(status='delivered').count(),
        'cancelled': query.filter_by(status='cancelled').count()
    }
    
    response = {
        'order_count': order_count,
        'total_revenue': total_revenue,
        'status_counts': status_counts,
    }
    
    # Admin için ek istatistikler
    if is_admin:
        # Düşük stok uyarıları
        low_stock = Product.query.filter(Product.stock < 10).all()
        response['low_stock'] = [{
            'id': p.id,
            'name': p.name,
            'stock': p.stock,
            'price': p.price
        } for p in low_stock]
        
        # Müşteri istatistikleri
        customer_count = Customer.query.count()
        new_customers = Customer.query.filter(Customer.created_at >= since_date).count()
        response['customer_stats'] = {
            'total': customer_count,
            'new': new_customers
        }
        
        # Ödeme istatistikleri
        payments = Payment.query.filter(Payment.created_at >= since_date).all()
        payment_methods = {}
        for p in payments:
            method = p.payment_method
            payment_methods[method] = payment_methods.get(method, 0) + p.amount
        response['payment_stats'] = payment_methods
    
    return jsonify(response)

# Satış grafikleri
@dashboard_api.route('/charts', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def charts():
    days = request.args.get('days', 30, type=int)
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Günlük satışlar
    daily_sales = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total).label('total')
    ).filter(Order.created_at >= since_date).group_by('date').all()
    
    # En çok satan ürünler
    top_products = db.session.query(
        Product.name,
        func.count(Order.id).label('count')
    ).join(Order).filter(Order.created_at >= since_date).group_by(Product.name).limit(5).all()
    
    return jsonify({
        'daily_sales': [{
            'date': str(day.date),
            'total': float(day.total)
        } for day in daily_sales],
        'top_products': [{
            'name': product.name,
            'count': product.count
        } for product in top_products]
    })
