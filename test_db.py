import sqlite3
import os

def test_database():
    db_name = 'sentinel_pro.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables found: {tables}")
    assert 'users' in tables
    assert 'audit_logs' in tables
    
    print("Test passed: Database schema is correct.")
    conn.close()

if __name__ == "__main__":
    test_database()
