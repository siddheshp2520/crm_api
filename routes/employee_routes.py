from flask import Blueprint, request, jsonify
from models.db import mysql  

employee_bp = Blueprint('employee_bp', __name__)

# ✅ Get All Employees
@employee_bp.route('/', methods=['GET'])
def get_employees():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")

    rows = cur.fetchall()
    employees = []

    for row in rows:
        employees.append({
            "eid": row[0],
            "empname": row[1],
            "jobtitle": row[2],
            "empcontact": row[3],
            "empemail": row[4],
            "address": row[5],
            "password": row[6],
            "empdate": str(row[7])
        })

    cur.close()
    return jsonify(employees)


# ✅ Add Employee
@employee_bp.route('/add', methods=['POST'])
def add_employee():
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO employee
        (empname, jobtitle, empcontact, empemail, address, pass, empdate)
        VALUES (%s,%s,%s,%s,%s,%s,NOW())
    """, (
        data.get('empname'),
        data.get('jobtitle'),
        data.get('empcontact'),
        data.get('empemail'),
        data.get('address'),
        data.get('pass')
    ))

    mysql.connection.commit()
    cur.close()

    return {"message": "Employee Added Successfully"}


# ✅ Delete Employee
@employee_bp.route('/delete/<int:eid>', methods=['DELETE'])
def delete_employee(eid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE eid=%s", (eid,))
    mysql.connection.commit()
    cur.close()

    return {"message": "Employee Deleted Successfully"}