# models/db.py

from flask_mysqldb import MySQL

mysql = MySQL()


def init_db(app):
    """Initialize MySQL with Flask app"""
    mysql.init_app(app)


def get_cursor():
    """Get DB cursor safely"""
    try:
        return mysql.connection.cursor()
    except Exception as e:
        raise Exception("Database connection failed")


def commit():
    mysql.connection.commit()


def rollback():
    try:
        mysql.connection.rollback()
    except Exception:
        pass


def close_cursor(cursor):
    if cursor:
        cursor.close()


def execute_query(query, params=None):
    """SELECT queries"""
    cursor = None
    try:
        cursor = get_cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Query failed: {str(e)}")
    finally:
        close_cursor(cursor)


def execute_commit(query, params=None):
    """INSERT / UPDATE / DELETE"""
    cursor = None
    try:
        cursor = get_cursor()
        cursor.execute(query, params or ())
        commit()
    except Exception as e:
        rollback()
        raise Exception(f"Commit failed: {str(e)}")
    finally:
        close_cursor(cursor)