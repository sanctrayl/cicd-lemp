import json
import os
import paho.mqtt.client as mqtt
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "chat/messages")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def save_to_db(nickname, text, client_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "INSERT INTO messages (nickname, message, client_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nickname, text, client_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Saved: {nickname}")
    except Exception as e:
        print(f"Database Error: {e}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        if 'nickname' in data and 'text' in data:
            save_to_db(data['nickname'], data['text'], data.get('clientId', ''))
    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client(client_id="db_logger_secure")
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print("Secure MQTT Logger Running...")
client.loop_forever()
