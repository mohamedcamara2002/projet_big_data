import psycopg2
import pandas as pd
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'inflation_db'),
        user=os.getenv('POSTGRES_USER', 'admin'),
        password=os.getenv('POSTGRES_PASSWORD', 'admin')
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
        );
        """)
        conn.commit()

def insert_data(conn, csv_path):
    df = pd.read_csv(csv_path)
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
            INSERT INTO inflation (country, country_code, year, inflation)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """, (row['Country'], row['Country Code'], row['Year'], row['Inflation']))
        conn.commit()

def main():
    csv_file = '/data/inflation.csv'  # chemin dans le container Docker
    conn = get_connection()
    create_table(conn)
    insert_data(conn, csv_file)
    print("Insertion des données terminée.")
    conn.close()

if __name__ == "__main__":
    main()
