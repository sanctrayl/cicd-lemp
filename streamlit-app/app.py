import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Sähköseuranta", layout="wide")

db_config = st.secrets["connections"]["mysql"]

def get_data():
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["username"],
            password=db_config["password"],
            database=db_config["database"]
        )

        query = "SELECT timestamp, price FROM spot_prices ORDER BY timestamp DESC LIMIT 50"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Virhe yhdistettäessä tietokantaan: {e}")
        return pd.DataFrame()

st.title("Sähköseuranta")

df = get_data()

if not df.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Hintakehitys (snt/kWh)")
        st.line_chart(df, x='timestamp', y='price')

    with col2:
        st.subheader("Datapisteet")
        st.dataframe(df)

        avg_price = df['price'].mean()
        st.metric(label="Keskihinta", value=f"{avg_price:.2f} c/kWh")
else:
    st.warning("Odota!")
