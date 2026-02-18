import socket
import sqlite3
from datetime import datetime
import threading

def init_db():
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents 
                 (id INTEGER PRIMARY KEY, ip TEXT, port INTEGER, time TEXT)''')
    conn.commit()
    conn.close()

def log_attack(ip, port):
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute("INSERT INTO incidents (ip, port, time) VALUES (?, ?, ?)",
              (ip, port, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def start_trap(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        while True:
            client, addr = server.accept()
            log_attack(addr[0], port)
            client.send(b"Access Denied. Security Protocol Active.\n")
            client.close()
    except Exception as e:
        print(f"Port {port} error: {e}")

if __name__ == "__main__":
    init_db()
    for p in [8080, 8888, 9999]:
     threading.Thread(target=start_trap, args=(p,)).start()
    print("Honeypot Engine is running...")
