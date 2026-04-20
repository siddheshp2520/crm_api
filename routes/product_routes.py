from flask import Blueprint, jsonify
from crm_api.models.db import mysql

product_bp = Blueprint('product_bp', __name__)

# ✅ Get All Products
@product_bp.route('/', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()

    # ✅ Explicit columns (BEST PRACTICE)
    cur.execute("""
        SELECT id, productcategary, productname, rentprice, unit,
               rackno, quantity, totalquantity, imageProperties,
               description, datetime, sessionid, hsn_no
        FROM product
    """)

    rows = cur.fetchall()
    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "category": row[1],
            "productname": row[2],
            "rentprice": row[3],
            "unit": row[4],
            "rackno": row[5],
            "quantity": row[6],
            "totalquantity": row[7],
            "imageProperties": row[8],
            "description": row[9],
            "datetime": str(row[10]),
            "sessionid": row[11],
            "hsn_no": row[12]
        })

    cur.close()
    return jsonify(products)