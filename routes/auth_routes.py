# auth_routes.py

from flask import Blueprint, request, jsonify
from models.db import mysql
import hashlib

# ── Blueprint ────────────────────────────────────────────────────────────────
auth_bp = Blueprint('auth_bp', __name__)


# ── Helper ───────────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    """SHA-256 hash a plain-text password."""
    return hashlib.sha256(password.encode()).hexdigest()


# =============================================================================
# TEST ROUTE  –  GET /api/auth/test
# =============================================================================
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Auth API Working Successfully ✅"}), 200


# =============================================================================
# LOGIN  –  GET & POST /api/auth/login
# =============================================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # ── Browser GET ───────────────────────────────────────────────────────
    if request.method == 'GET':
        username = request.args.get('username', '').strip()
        password = request.args.get('password', '').strip()

        # No params = show usage hint
        if not username or not password:
            return jsonify({
                "message": "Login route is working ✅",
                "note": "Pass credentials as query params (GET) or JSON body (POST)",
                "GET_example":  "/api/auth/login?username=admin&password=1234",
                "POST_example": {
                    "username": "admin",
                    "password": "1234"
                }
            }), 200

    # ── Postman / Frontend POST ───────────────────────────────────────────
    else:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Request body must be JSON ❌"}), 400

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

    # ── Shared validation ─────────────────────────────────────────────────
    if not username or not password:
        return jsonify({"message": "Username and Password are required ❌"}), 400

    if len(username) > 255 or len(password) > 255:
        return jsonify({"message": "Invalid input length ❌"}), 400

    # ── Hash password ─────────────────────────────────────────────────────
    hashed_pw = hash_password(password)

    # ── Query DB ──────────────────────────────────────────────────────────
    cursor = None
    try:
        cursor = mysql.connection.cursor()

        # First check if username exists
        cursor.execute("""
            SELECT id, name, username, role, status, emailaddress, password
            FROM login
            WHERE username = %s
        """, (username,))
        user = cursor.fetchone()

    except Exception as e:
        return jsonify({"message": "Database error ❌", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

    # ── Username not found ────────────────────────────────────────────────
    if not user:
        return jsonify({"message": "Invalid Username or Password ❌"}), 401

    user_id, name, uname, role, status, email, db_password = user

    # ── Check status first ────────────────────────────────────────────────
    if not status or status.lower() != 'active':
        return jsonify({
            "message": "Account is inactive. Please contact admin ❌",
            "status": status
        }), 403

    # ── Compare password (handle both plain text and hashed) ──────────────
    password_match = (db_password == hashed_pw) or (db_password == password)

    if not password_match:
        return jsonify({"message": "Invalid Username or Password ❌"}), 401

    # ── Success ───────────────────────────────────────────────────────────
    return jsonify({
        "message": "Login Successful ✅",
        "user": {
            "id":       user_id,
            "name":     name,
            "username": uname,
            "email":    email,
            "role":     role,
            "status":   status
        }
    }), 200


# =============================================================================
# LOGIN TEST FOR BROWSER  –  GET /api/auth/login-test?username=x&password=y
# =============================================================================
@auth_bp.route('/login-test', methods=['GET'])
def login_test():
    username = request.args.get('username', '').strip()
    password = request.args.get('password', '').strip()

    if not username or not password:
        return jsonify({
            "message": "Provide username and password as query params ❌",
            "example": "/api/auth/login-test?username=admin&password=1234"
        }), 400

    hashed_pw = hash_password(password)

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, name, username, role, status, emailaddress, password
            FROM login
            WHERE username = %s
        """, (username,))
        user = cursor.fetchone()

    except Exception as e:
        return jsonify({"message": "Database error ❌", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

    if not user:
        return jsonify({"message": "Invalid Username or Password ❌"}), 401

    user_id, name, uname, role, status, email, db_password = user

    if not status or status.lower() != 'active':
        return jsonify({
            "message": "Account is inactive. Please contact admin ❌",
            "status": status
        }), 403

    # Compare both hashed and plain
    password_match = (db_password == hashed_pw) or (db_password == password)

    if not password_match:
        return jsonify({"message": "Invalid Username or Password ❌"}), 401

    return jsonify({
        "message": "Login Successful ✅",
        "user": {
            "id":       user_id,
            "name":     name,
            "username": uname,
            "email":    email,
            "role":     role,
            "status":   status
        }
    }), 200


# =============================================================================
# GET ALL USERS  –  GET /api/auth/users
# =============================================================================
@auth_bp.route('/users', methods=['GET'])
def get_users():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, type, company_id, name, emailaddress,
                   contact, address, username, role, status, registrationdate
            FROM login
            ORDER BY registrationdate DESC
        """)
        rows = cursor.fetchall()

    except Exception as e:
        return jsonify({"message": "Database error ❌", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

    users = [
        {
            "id":               row[0],
            "type":             row[1],
            "company_id":       row[2],
            "name":             row[3],
            "email":            row[4],
            "contact":          row[5],
            "address":          row[6],
            "username":         row[7],
            "role":             row[8],
            "status":           row[9],
            "registrationdate": str(row[10]) if row[10] else None
        }
        for row in rows
    ]

    return jsonify({
        "message": "Users fetched successfully ✅",
        "total":   len(users),
        "users":   users
    }), 200


# =============================================================================
# HASH TEST  –  GET /api/auth/hash-test?password=1234
# =============================================================================
@auth_bp.route('/hash-test', methods=['GET'])
def hash_test():
    password = request.args.get('password', '').strip()
    if not password:
        return jsonify({"message": "Provide password as query param ❌"}), 400

    return jsonify({
        "plain":        password,
        "hashed":       hash_password(password),
        "hash_length":  len(hash_password(password))
    }), 200


# =============================================================================
# ONE TIME PASSWORD MIGRATION  –  GET /api/auth/migrate-passwords
# RUN ONCE THEN DELETE THIS ROUTE
# =============================================================================
@auth_bp.route('/migrate-passwords', methods=['GET'])
def migrate_passwords():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, password FROM login")
        users = cursor.fetchall()

        count = 0
        for user_id, plain_pw in users:
            if not plain_pw:
                continue
            # Skip already hashed (SHA-256 = 64 chars)
            if len(plain_pw) == 64:
                continue
            hashed = hash_password(plain_pw)
            cursor.execute(
                "UPDATE login SET password=%s WHERE id=%s",
                (hashed, user_id)
            )
            count += 1

        mysql.connection.commit()

    except Exception as e:
        return jsonify({"message": "Migration failed ❌", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

    return jsonify({
        "message": "Passwords migrated successfully ✅",
        "updated": count
    }), 200