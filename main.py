from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'Unread'
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    db = get_db()

    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            book_id = request.form.get('book_id')
            db.execute('DELETE FROM books WHERE id = ?', (book_id,))
            db.commit()
            message = 'Book deleted successfully.'
        elif request.form.get('action') == 'update':
            book_id = request.form.get('book_id')
            new_status = request.form.get('status')
            db.execute('UPDATE books SET status = ? WHERE id = ?', (new_status, book_id))
            db.commit()
            message = 'Book status updated.'
        else:
            title = request.form.get('title')
            if title:
                db.execute('INSERT INTO books (title) VALUES (?)', (title,))
                db.commit()
                message = 'Book added successfully.'
            else:
                message = 'Missing book title.'

    books = db.execute('SELECT * FROM books').fetchall()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Book Tracker</title></head>
        <body>
            <h2>Add Book</h2>
            <form method="POST" action="/">
                <input type="text" name="title" placeholder="Enter a book title" required>
                <input type="submit" value="Add Book">
            </form>
            <p>{{ message }}</p>
            <h3>Book List</h3>
            {% if books %}
                <table border="1">
                    <tr><th>Title</th><th>Status</th><th>Update</th><th>Delete</th></tr>
                    {% for book in books %}
                    <tr>
                        <td>{{ book['title'] }}</td>
                        <td>{{ book['status'] }}</td>
                        <td>
                            <form method="POST" action="/">
                                <input type="hidden" name="book_id" value="{{ book['id'] }}">
                                <select name="status">
                                    <option value="Unread" {% if book['status'] == 'Unread' %}selected{% endif %}>Unread</option>
                                    <option value="Reading" {% if book['status'] == 'Reading' %}selected{% endif %}>Reading</option>
                                    <option value="Read" {% if book['status'] == 'Read' %}selected{% endif %}>Read</option>
                                </select>
                                <input type="hidden" name="action" value="update">
                                <input type="submit" value="Update">
                            </form>
                        </td>
                        <td>
                            <form method="POST" action="/">
                                <input type="hidden" name="book_id" value="{{ book['id'] }}">
                                <input type="hidden" name="action" value="delete">
                                <input type="submit" value="Delete">
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No books in your list yet.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, books=books)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
