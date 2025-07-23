from flask import Flask, send_from_directory
from myproject.api.models import db
from myproject.api.routes import api
from myproject.api.product import product_api
from myproject.api.payment import payment_api
from myproject.api.delivery import delivery_api
from myproject.api.dashboard import dashboard_api
from myproject.api.logs import logs_api
from myproject.api.auto_message import auto_message_api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from myproject.config import Config
import os

app = Flask(__name__, static_folder='web/dist')
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)
jwt = JWTManager(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')






app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(product_api, url_prefix='/api/products')
app.register_blueprint(payment_api, url_prefix='/api/payments')
app.register_blueprint(delivery_api, url_prefix='/api/delivery')
app.register_blueprint(dashboard_api, url_prefix='/api/dashboard')
app.register_blueprint(logs_api, url_prefix='/api/logs')
app.register_blueprint(auto_message_api, url_prefix='/api/auto-message')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)