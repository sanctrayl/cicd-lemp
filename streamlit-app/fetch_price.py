import os
import sys
import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

API_URL = "https://api.spot-hinta.fi/JustNow"

def fetch_and_store():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        price = data.get('PriceWithTax')

        timestamp = datetime.now()

        if price is None:
            print("Error: Could not find PriceWithTax in response")
            return

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "INSERT INTO spot_prices (price, timestamp) VALUES (%s, %s)"
        cursor.execute(query, (price, timestamp))
        conn.commit()

        print(f"Success: Stored {price} c/kWh at {timestamp}")

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}", file=sys.stderr)
    except mysql.connector.Error as err:
        print(f"Database Error: {err}", file=sys.stderr)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fetch_and_store()
