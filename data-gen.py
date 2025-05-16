import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_inventory(num_items):
    db = connect_db()
    for i in range(num_items):
        name = f'Item {i}'
        category = f'Category {i % 3}'
        quantity = i * 5
        db.execute('INSERT INTO inventory (name, category, quantity) VALUES (?, ?, ?)', (name, category, quantity))
    db.commit()
    print(f'{num_items} inventory items added.')
    db.close()

if __name__ == '__main__':
    generate_test_inventory(10)
