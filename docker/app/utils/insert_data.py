import psycopg2
import csv
from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="inflation_db",
        user="admin",
        password="admin"
    )

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS inflation (
            id SERIAL PRIMARY KEY,
            country VARCHAR(100),
            country_code VARCHAR(3),
            year INTEGER,
            inflation FLOAT
        )
        """)
        conn.commit()

def insert_data(conn, data_path):
    df = pd.read_csv(data_path)
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
            INSERT INTO inflation (country, country_code, year, inflation)
            VALUES (%s, %s, %s, %s)
            """, (row['Country'], row['Country Code'], row['Year'], row['Inflation']))
        conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    create_table(conn)
    insert_data(conn, "_data/inflation.csv")  # Assurez-vous que le fichier est présent
    conn.close()

