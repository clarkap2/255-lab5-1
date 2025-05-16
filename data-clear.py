import sqlite3
import re

DATABASE = 'demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def is_junk_title(title):
    junk_keywords = [
        'alert(', '<script', '--', 'UNION', 'SELECT', 'sqlmap', '%3c', '%3e'
    ]
    for keyword in junk_keywords:
        if keyword.lower() in title.lower():
            return True

    if re.fullmatch(r'[a-z0-9]{5,10}', title):
        return True

    return False

def clear_junk_books():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title FROM books")
    rows = cursor.fetchall()

    junk_ids = [row[0] for row in rows if is_junk_title(row[1])]

    for junk_id in junk_ids:
        cursor.execute("DELETE FROM books WHERE id = ?", (junk_id,))
    db.commit()
    print(f"Deleted {len(junk_ids)} junk books.")
    db.close()

if __name__ == '__main__':
    clear_junk_books()
