import sqlite3

DATABASE = 'demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_books(num_books):
    db = connect_db()
    for i in range(num_books):
        title = f'Test Book {i}'
        db.execute('INSERT INTO books (title, status) VALUES (?, ?)', (title, 'Unread'))
    db.commit()
    print(f'{num_books} test books added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_books(10)
