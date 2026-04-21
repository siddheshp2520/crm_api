# app.py

from flask import Flask, jsonify
from flask_cors import CORS

# Config & DB
from config import Config
from models.db import init_db

# Routes
from routes.customer_routes import customer_bp
from routes.company_routes import company_bp
from routes.bill_routes import bill_bp
from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp
from routes.product_routes import product_bp
from routes.leads_routes import leads_bp


def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_object(Config)

    # Init DB
    init_db(app)

    # Enable CORS
    CORS(app)

    # Register Blueprints
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(company_bp,  url_prefix='/api/company')
    app.register_blueprint(bill_bp,     url_prefix='/api/bills')
    app.register_blueprint(auth_bp,     url_prefix='/api/auth')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')
    app.register_blueprint(product_bp,  url_prefix='/api/products')
    app.register_blueprint(leads_bp,    url_prefix='/api/leads')

    # Routes
    @app.route('/')
    def home():
        return jsonify({
            "message": "🚀 CRM API Running Successfully",
            "status": "online",
        })

    @app.route('/test')
    def test():
        return jsonify({"message": "Server Working ✅"})

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Route not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"message": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"message": "Internal server error"}), 500

    return app


# Required for Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)