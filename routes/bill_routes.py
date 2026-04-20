from flask import Blueprint, request, jsonify
from models.db import mysql

bill_bp = Blueprint('bill_bp', __name__)

# ✅ Get All Bills
@bill_bp.route('/', methods=['GET'])
def get_bills():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills")

    rows = cur.fetchall()
    bills = []

    for row in rows:
        bills.append({
            "id": row[0],
            "bill_no": row[1],
            "bill_title": row[2],
            "vendor_name": row[3],
            "amount": row[4],
            "paidamount": row[5],
            "due_on": str(row[6]),
            "due_date": str(row[7]),
            "balance_due": row[8],
            "status": row[9],
            "created_at": str(row[10]),
            "updated_at": str(row[11]),
            "company_id": row[12]
        })

    cur.close()
    return jsonify(bills)