# crm_api/models/db.py

from flask_mysqldb import MySQL

# ── MySQL Object ──────────────────────────────────────────────────────────────
mysql = MySQL()


def init_db(app):
    """Initialize MySQL with Flask app."""
    mysql.init_app(app)


def get_cursor():
    """Get a fresh database cursor."""
    return mysql.connection.cursor()


def commit():
    """Commit pending changes to database."""
    mysql.connection.commit()


def close_cursor(cursor):
    """Close cursor safely."""
    if cursor:
        cursor.close()


def rollback():
    """Rollback on error."""
    try:
        mysql.connection.rollback()
    except Exception:
        pass


def execute_query(query, params=None):
    """
    Run a query and return all rows.
    Use for SELECT statements.
    """
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
    """
    Run a query and commit.
    Use for INSERT / UPDATE / DELETE statements.
    """
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