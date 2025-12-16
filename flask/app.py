from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
        result = cursor.fetchone()
        db_time = result[0].strftime("%Y-%m-%d %H:%M:%S")

        cursor.close()
        conn.close()
        
        return f"""
        <html>
            <head><title>Main Page</title></head>
            <body style='font-family: sans-serif; text-align: center; margin-top: 50px;'>
                <style>
                    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0a1128 0%, #001f54 25%, #034078 50%, #001f54 75%, #fefcfb 100%);
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    text-align: center;
                    max-width: 600px;
                    width: 90%;
                }}
                h1 {{ margin-bottom: 10px; font-size: 2.5rem; letter-spacing: 2px; text-shadow: 0 2px 5px rgba(0,0,0,0.3); }}
                .time-display {{
                    font-size: 1.1rem;
                    color: #a8c0ff;
                    margin-bottom: 40px;
                    font-weight: 300;
                    padding-bottom: 20px;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                }}
                .button-group {{
                    display: flex;
                    gap: 20px;
                    justify-content: center;
                    flex-wrap: wrap;
                }}
                .btn {{
                    text-decoration: none;
                    padding: 15px 30px;
                    border-radius: 50px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    font-size: 0.9rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    min-width: 160px;
                    display: inline-block;
                }}
                .btn-chat {{
                    background: linear-gradient(to right, #73ba9b, #003e1f);
                    color: white;
                }}
                .btn-data {{
                    background: linear-gradient(to right, #001427, #708d81);
                    color: white;
                }}
                .btn:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>LEMP</h1>
                <div class="time-display">
                    Palvelimen aika: {db_time}
                </div>
                <div class="button-group">
                    <a href="/chat/" class="btn btn-chat">Avaa Chat</a>
                    <a href="/data-analysis/" class="btn btn-data">Analyysi</a>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1 style='color:white; text-align:center;'>Virhe tietokantayhteydessä: {e}</h1>"


def get_k8s_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD', 'apppassword123'),
        database=os.getenv('DB_NAME', 'appdb')
    )

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/init-db')
def init_db():
    try:
        conn = get_k8s_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database ready."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    try:
        conn = get_k8s_db_connection()
        
        if request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                conn.close()
                return jsonify({"error": "Name and email required"}), 400

            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "User saved successfully!"}), 201

        else:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users ORDER BY id DESC")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import psutil

@app.route('/api/system')
def system_status():
    """New Feature: Returns server system stats"""
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    return jsonify({
        "cpu_percent": cpu_usage,
        "memory_percent": memory.percent,
        "status": "online"
    })
