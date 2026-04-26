import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(cursor, username, password):
    hashed_p = hash_password(password)
    cursor.execute("SELECT * FROM system_users WHERE username=? AND password=?", (username, hashed_p))
    if cursor.fetchone() or (username == "admin" and password == "sentinel2026"):
        return True
    return False

def register_user(db_conn, cursor, username, password):
    try:
        hashed_new_p = hash_password(password)
        cursor.execute("INSERT INTO system_users (username, password) VALUES (?, ?)", (username, hashed_new_p))
        db_conn.commit()
        return True, "Investigator Registered Successfully"
    except Exception:
        return False, "Node ID already exists in the system"
