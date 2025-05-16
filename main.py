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
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
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
            db.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
            db.commit()
            message = 'Item deleted.'

        elif action == 'adjust_quantity':
            item_id = request.form.get('item_id')
            amount = int(request.form.get('adjust_amount', 0))
            db.execute('UPDATE inventory SET quantity = quantity + ? WHERE id = ?', (amount, item_id))
            db.commit()
            message = 'Quantity adjusted.'

        else:  # Add item
            name = request.form.get('name')
            category = request.form.get('category')
            quantity = int(request.form.get('quantity', 0))
            if name and category:
                db.execute('INSERT INTO inventory (name, category, quantity) VALUES (?, ?, ?)', (name, category, quantity))
                db.commit()
                message = 'Item added.'
            else:
                message = 'Missing name or category.'

    items = db.execute('SELECT * FROM inventory').fetchall()

    return render_template_string('''
        <h2>Store Inventory</h2>
        <form method="POST">
            <label>Item Name:</label><br>
            <input type="text" name="name" required><br>
            <label>Category:</label><br>
            <input type="text" name="category" required><br>
            <label>Initial Quantity:</label><br>
            <input type="number" name="quantity" value="0"><br><br>
            <input type="submit" value="Add Item">
        </form>
        <p>{{ message }}</p>

        {% if items %}
            <table border="1">
                <tr>
                    <th>Name</th><th>Category</th><th>Quantity</th><th>Adjust</th><th>Delete</th>
                </tr>
                {% for item in items %}
                    <tr>
                        <td>{{ item['name'] }}</td>
                        <td>{{ item['category'] }}</td>
                        <td>{{ item['quantity'] }}</td>
                        <td>
                            <form method="POST">
                                <input type="hidden" name="item_id" value="{{ item['id'] }}">
                                <input type="number" name="adjust_amount" value="1">
                                <input type="hidden" name="action" value="adjust_quantity">
                                <input type="submit" value="Update Qty">
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
            <p>No items found.</p>
        {% endif %}
    ''', message=message, items=items)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
