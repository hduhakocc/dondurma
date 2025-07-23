from flask import Blueprint, request, jsonify
from .models import db, User, Customer, Order
from .utils import role_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)


# Kullanıcı girişi
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Geçersiz kullanıcı adı veya şifre'}), 401

# Yeni kullanıcı kaydı (sadece admin)
@api.route('/register', methods=['POST'])
@role_required(['admin'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': 'Kullanıcı adı zaten mevcut'}), 400
    user = User(username=data['username'], role=data.get('role', 'member'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Kullanıcı kaydedildi', 'id': user.id}), 201


# Müşteri ekleme (sadece girişli kullanıcılar)
@api.route('/customers', methods=['POST'])
@jwt_required()
def add_customer():
    data = request.json
    customer = Customer(
        name=data['name'],
        surname=data['surname'],
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'msg': 'Müşteri eklendi', 'id': customer.id}), 201

# Müşteri listeleme (arama ve filtreleme için basit örnek)
@api.route('/customers', methods=['GET'])
@jwt_required()
def list_customers():
    query = Customer.query
    name = request.args.get('name')
    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))
    customers = query.all()
    return jsonify([
        {'id': c.id, 'name': c.name, 'surname': c.surname, 'phone': c.phone, 'address': c.address}
        for c in customers
    ])


# Sipariş ekleme (sadece girişli kullanıcılar)
@api.route('/orders', methods=['POST'])
@jwt_required()
def add_order():
    data = request.json
    order = Order(
        customer_id=data['customer_id'],
        user_id=get_jwt_identity()['id'],
        total=data['total'],
        status='pending'
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'msg': 'Sipariş eklendi', 'id': order.id}), 201

# Sipariş listeleme (filtreleme için basit örnek)
@api.route('/orders', methods=['GET'])
@jwt_required()
def list_orders():
    customer_id = request.args.get('customer_id')
    query = Order.query
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    orders = query.all()
    return jsonify([
        {'id': o.id, 'customer_id': o.customer_id, 'user_id': o.user_id, 'total': o.total, 'status': o.status}
        for o in orders
    ])
