from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS shopping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'Needed'
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    db = get_db()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            item_id = request.form.get('item_id')
            db.execute('DELETE FROM shopping WHERE id = ?', (item_id,))
            db.commit()
            message = 'Item deleted.'

        elif action == 'update':
            item_id = request.form.get('item_id')
            new_status = request.form.get('status')
            db.execute('UPDATE shopping SET status = ? WHERE id = ?', (new_status, item_id))
            db.commit()
            message = 'Item status updated.'

        else:
            name = request.form.get('name')
            quantity = int(request.form.get('quantity', 1))
            if name:
                db.execute('INSERT INTO shopping (name, quantity) VALUES (?, ?)', (name, quantity))
                db.commit()
                message = 'Item added.'
            else:
                message = 'Missing item name.'

    items = db.execute('SELECT * FROM shopping').fetchall()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Shopping List</title></head>
        <body>
            <h2>Shopping List</h2>
            <form method="POST">
                <input type="text" name="name" placeholder="Item name" required>
                <input type="number" name="quantity" min="1" value="1">
                <input type="submit" value="Add Item">
            </form>
            <p>{{ message }}</p>
            {% if items %}
            <table border="1">
                <tr><th>Name</th><th>Qty</th><th>Status</th><th>Update</th><th>Delete</th></tr>
                {% for item in items %}
                <tr>
                    <td>{{ item['name'] }}</td>
                    <td>{{ item['quantity'] }}</td>
                    <td>{{ item['status'] }}</td>
                    <td>
                        <form method="POST">
                            <input type="hidden" name="item_id" value="{{ item['id'] }}">
                            <select name="status">
                                <option value="Needed" {% if item['status'] == 'Needed' %}selected{% endif %}>Needed</option>
                                <option value="Purchased" {% if item['status'] == 'Purchased' %}selected{% endif %}>Purchased</option>
                                <option value="Not Available" {% if item['status'] == 'Not Available' %}selected{% endif %}>Not Available</option>
                            </select>
                            <input type="hidden" name="action" value="update">
                            <input type="submit" value="Update">
                        </form>
                    </td>
                    <td>
                        <form method="POST">
                            <input type="hidden" name="item_id" value="{{ item['id'] }}">
                            <input type="hidden" name="action" value="delete">
                            <input type="submit" value="Delete">
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>No shopping items yet.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, items=items)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
