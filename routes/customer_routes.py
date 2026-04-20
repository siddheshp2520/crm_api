from flask import Blueprint, request, jsonify
from crm_api.models.db import mysql

customer_bp = Blueprint('customer_bp', __name__)


# ✅ Get All Customers (FULL DATA)
@customer_bp.route('/', methods=['GET'])
def get_customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer")

    rows = cur.fetchall()
    customers = []

    for row in rows:
        customers.append({
            "id": row[0],
            "username": row[1],
            "schoolname": row[2],
            "gst_no": row[3],
            "email": row[4],
            "contact": row[5],
            "alt_contact": row[6],
            "address": row[7],
            "successorder": row[8],
            "datetime": str(row[9])
        })

    cur.close()
    return jsonify(customers)