from flask import Blueprint, request, jsonify
from models.db import mysql

leads_bp = Blueprint('leads_bp', __name__)


# ==============================
# ✅ GET ALL LEADS
# ==============================
@leads_bp.route('/', methods=['GET'])
def get_leads():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM leads WHERE is_deleted = 0")

    rows = cur.fetchall()
    leads = []

    for row in rows:
        leads.append({
            "id": row[0],
            "enquiry_number": row[1],
            "client_id": row[2],
            "login_id": row[3],
            "title": row[4],
            "contact_person": row[5],
            "contact_number": row[6],
            "designation": row[7],
            "requirement": row[8],
            "description": row[9],
            "status": row[10],
            "enquiry_source": row[11],
            "product": row[12],
            "is_deleted": row[13],
            "created_at": str(row[14]),
            "updated_at": str(row[15])
        })

    cur.close()
    return jsonify(leads)


# ==============================
# ✅ ADD NEW LEAD
# ==============================
@leads_bp.route('/add', methods=['POST'])
def add_lead():
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO leads
        (enquiry_number, client_id, login_id, title, contact_person,
         contact_number, designation, requirement, description,
         status, enquiry_source, product, is_deleted, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,NOW())
    """, (
        data.get('enquiry_number'),
        data.get('client_id'),
        data.get('login_id'),
        data.get('title'),
        data.get('contact_person'),
        data.get('contact_number'),
        data.get('designation'),
        data.get('requirement'),
        data.get('description'),
        data.get('status'),
        data.get('enquiry_source'),
        data.get('product')
    ))

    mysql.connection.commit()
    cur.close()

    return {"message": "Lead Added Successfully"}


# ==============================
# ✅ GET SINGLE LEAD
# ==============================
@leads_bp.route('/<int:id>', methods=['GET'])
def get_lead(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM leads WHERE id=%s", (id,))
    row = cur.fetchone()
    cur.close()

    if row:
        return {
            "id": row[0],
            "title": row[4],
            "contact_person": row[5],
            "status": row[10]
        }
    else:
        return {"message": "Lead Not Found"}, 404


# ==============================
# ✅ UPDATE LEAD
# ==============================
@leads_bp.route('/update/<int:id>', methods=['PUT'])
def update_lead(id):
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE leads
        SET title=%s, contact_person=%s, contact_number=%s,
            requirement=%s, status=%s, updated_at=NOW()
        WHERE id=%s
    """, (
        data.get('title'),
        data.get('contact_person'),
        data.get('contact_number'),
        data.get('requirement'),
        data.get('status'),
        id
    ))

    mysql.connection.commit()
    cur.close()

    return {"message": "Lead Updated Successfully"}


# ==============================
# ✅ DELETE (SOFT DELETE)
# ==============================
@leads_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_lead(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE leads SET is_deleted=1 WHERE id=%s
    """, (id,))

    mysql.connection.commit()
    cur.close()

    return {"message": "Lead Deleted Successfully"}