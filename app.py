from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
DB_PATH = 'data.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                liters REAL,
                price REAL,
                fuel_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sale', methods=['POST'])
def sale():
    try:
        liters = float(request.form['liters'])
        price = float(request.form['price'])
        fuel_type = request.form['fuel_type']
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sales (liters, price, fuel_type) VALUES (?, ?, ?)", (liters, price, fuel_type))
        conn.commit()
        conn.close()

        return redirect('/sales')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/sales')
def sales():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sales ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('sales.html', sales=rows)

@app.route('/report')
def report():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT SUM(liters), SUM(price) FROM sales")
    total_liters, total_price = c.fetchone()
    conn.close()
    return render_template('report.html', total_liters=total_liters, total_price=total_price)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
