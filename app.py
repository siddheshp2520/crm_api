# app.py

from flask import Flask, jsonify
from flask_cors import CORS

# ✅ Config + DB
from config import Config        # ← Remove crm_api.
from models.db import mysql      # ← Remove crm_api.

# ✅ Import All Routes
from routes.customer_routes import customer_bp    # ← Remove crm_api.
from routes.company_routes  import company_bp     # ← Remove crm_api.
from routes.bill_routes     import bill_bp        # ← Remove crm_api.
from routes.auth_routes     import auth_bp        # ← Remove crm_api.
from routes.employee_routes import employee_bp    # ← Remove crm_api.
from routes.product_routes  import product_bp     # ← Remove crm_api.
from routes.leads_routes    import leads_bp       # ← Remove crm_api.


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    mysql.init_app(app)
    CORS(app)

    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(company_bp,  url_prefix='/api/company')
    app.register_blueprint(bill_bp,     url_prefix='/api/bills')
    app.register_blueprint(auth_bp,     url_prefix='/api/auth')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')
    app.register_blueprint(product_bp,  url_prefix='/api/products')
    app.register_blueprint(leads_bp,    url_prefix='/api/leads')

    @app.route('/')
    def home():
        return jsonify({
            "message": "🚀 CRM API Running Successfully",
            "status":  "online ✅",
            "apis": [
                "/api/customers",
                "/api/company",
                "/api/bills",
                "/api/auth/login",
                "/api/auth/users",
                "/api/employee",
                "/api/products",
                "/api/leads"
            ]
        }), 200

    @app.route('/test')
    def test():
        return jsonify({"message": "Server Working ✅"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Route not found ❌"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"message": "Method not allowed ❌"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"message": "Internal server error ❌"}), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=False)