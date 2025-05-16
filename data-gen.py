import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_items(num_items):
    db = connect_db()
    for i in range(num_items):
        name = f'Test Item {i}'
        db.execute('INSERT INTO shopping (name, quantity, status) VALUES (?, ?, ?)', (name, i+1, 'Needed'))
    db.commit()
    print(f'{num_items} test shopping items added.')
    db.close()

if __name__ == '__main__':
    generate_test_items(10)
