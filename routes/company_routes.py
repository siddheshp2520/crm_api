from flask import Blueprint, request, jsonify
from crm_api.models.db import mysql

company_bp = Blueprint('company_bp', __name__)


# ✅ Get All Companies
@company_bp.route('/', methods=['GET'])
def get_companies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, contact FROM company")

    rows = cur.fetchall()
    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "contact": row[3]
        })

    cur.close()
    return jsonify(data)


# ✅ Add Company
@company_bp.route('/add', methods=['POST'])
def add_company():
    data = request.json
    name = data['name']
    email = data['email']
    contact = data.get('contact', '')

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO company(name, email, contact, created_at) VALUES(%s,%s,%s,NOW())",
        (name, email, contact)
    )
    mysql.connection.commit()
    cur.close()

    return {"message": "Company Added Successfully"}