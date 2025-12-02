from flask import Flask
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
