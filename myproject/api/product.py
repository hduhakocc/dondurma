from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Product
from .utils import role_required

product_api = Blueprint('product_api', __name__)

# Ürün ekleme (sadece admin)
@product_api.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def add_product():
    data = request.json
    product = Product(
        name=data['name'],
        price=data['price'],
        stock=data['stock'],
        barcode=data.get('barcode')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'msg': 'Ürün eklendi', 'id': product.id}), 201

# Ürün listeleme (herkes)
@product_api.route('/', methods=['GET'])
@jwt_required()
def list_products():
    products = Product.query.all()
    return jsonify([
        {'id': p.id, 'name': p.name, 'price': p.price, 'stock': p.stock, 'barcode': p.barcode}
        for p in products
    ])

# Stok güncelleme (sadece admin)
@product_api.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'msg': 'Ürün bulunamadı'}), 404
    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.barcode = data.get('barcode', product.barcode)
    db.session.commit()
    return jsonify({'msg': 'Ürün güncellendi', 'id': product.id}), 200
