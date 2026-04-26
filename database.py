import sqlite3

def setup_database_infrastructure():
    connection = sqlite3.connect('sentinel_enterprise.db', check_same_thread=False)
    db_cursor = connection.cursor()

    # User Credentials Table
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS system_users
                         (
                             uid
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             username
                             TEXT
                             UNIQUE,
                             password
                             TEXT
                         )''')

    # Comprehensive Audit Logging Table
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS universal_audit_logs
                         (
                             log_id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             user
                             TEXT,
                             timestamp
                             TEXT,
                             module
                             TEXT,
                             entity
                             TEXT,
                             result
                             TEXT,
                             risk_score
                             TEXT,
                             action_taken
                             TEXT
                         )''')

    connection.commit()
    return connection, db_cursor


def commit_audit_log(db_conn, cursor, user, module, entity, status, score, action="LOG_ONLY"):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    operator = user if user else "SYSTEM_AUTO"
    cursor.execute(
        "INSERT INTO universal_audit_logs (user, timestamp, module, entity, result, risk_score, action_taken) VALUES (?,?,?,?,?,?,?)",
        (operator, now, module, entity, status, score, action))
    db_conn.commit()

# Initialize connection and cursor
db_conn, cursor = setup_database_infrastructure()
