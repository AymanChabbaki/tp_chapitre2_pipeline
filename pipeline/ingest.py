import pandas as pd
import duckdb
import os

def ingest_data():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "ventes.csv")
    db_path = os.path.join(os.path.dirname(__file__), "..", "ventes.duckdb")
    
    print(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Writing data to {db_path} in table 'ventes_raw'...")
    con = duckdb.connect(db_path)
    con.execute("CREATE OR REPLACE TABLE ventes_raw AS SELECT * FROM df")
    con.close()
    print("Ingestion completed successfully!")

if __name__ == "__main__":
    ingest_data()
