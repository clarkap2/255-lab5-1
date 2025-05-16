import sqlite3
import re

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def is_junk_entry(name):
    patterns = ['<script', 'alert(', '--', 'sqlmap', 'UNION']
    for pattern in patterns:
        if pattern.lower() in name.lower():
            return True
    if re.fullmatch(r'[a-z0-9]{5,10}', name):
        return True
    return False

def clear_junk_items():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM shopping")
    rows = cursor.fetchall()

    junk_ids = [row[0] for row in rows if is_junk_entry(row[1])]

    for item_id in junk_ids:
        cursor.execute("DELETE FROM shopping WHERE id = ?", (item_id,))
    db.commit()
    print(f"Deleted {len(junk_ids)} junk shopping items.")
    db.close()

if __name__ == '__main__':
    clear_junk_items()
