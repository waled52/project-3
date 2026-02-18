from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_logs():
    conn = sqlite3.connect('attacks.db')
    conn.row_factory = sqlite3.Row
    logs = conn.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT 15").fetchall()
    conn.close()
    return logs

@app.route('/')
def index():
    return render_template('index.html', attacks=get_logs())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
