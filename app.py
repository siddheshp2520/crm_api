from flask import Flask
from flask_cors import CORS

# ✅ Config + DB
from crm_api.config import Config
from crm_api.models.db import mysql

# ✅ Import All Routes
from crm_api.routes.customer_routes import customer_bp
from crm_api.routes.company_routes import company_bp
from crm_api.routes.bill_routes import bill_bp
from crm_api.routes.auth_routes import auth_bp
from crm_api.routes.employee_routes import employee_bp
from crm_api.routes.product_routes import product_bp
from crm_api.routes.leads_routes import leads_bp   # ✅ NEW

def create_app():
    app = Flask(__name__)

    # ✅ Load Config
    app.config.from_object(Config)

    # ✅ Init MySQL
    mysql.init_app(app)

    # ✅ Enable CORS
    CORS(app)

    # ===============================
    # ✅ Register All Blueprints
    # ===============================
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(company_bp, url_prefix='/api/company')
    app.register_blueprint(bill_bp, url_prefix='/api/bills')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(leads_bp, url_prefix='/api/leads')  # ✅ NEW

    # ===============================
    # ✅ HOME ROUTE
    # ===============================
    @app.route('/')
    def home():
        return {
            "message": "🚀 CRM API Running Successfully",
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
        }

    # ===============================
    # ✅ SERVER TEST
    # ===============================
    @app.route('/test')
    def test():
        return {"message": "Server Working ✅"}

    return app


# ===============================
# ✅ RUN SERVER
# ===============================
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)