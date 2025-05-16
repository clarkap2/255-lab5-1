import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def clear_inventory():
    db = connect_db()
    db.execute("DELETE FROM inventory WHERE name LIKE 'Item %'")
    db.commit()
    print('Test inventory items cleared.')
    db.close()

if __name__ == '__main__':
    clear_inventory()
