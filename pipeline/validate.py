import duckdb
import os

def validate_data():
    db_path = os.path.join(os.path.dirname(__file__), "..", "ventes.duckdb")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
        
    con = duckdb.connect(db_path)
    
    # 1. Vérifier que la table ventes_raw existe
    tables = con.execute("SHOW TABLES").fetchall()
    table_names = [table[0] for table in tables]
    if "ventes_raw" not in table_names:
        con.close()
        raise ValueError("La table 'ventes_raw' n'existe pas dans la base de données.")
        
    # 2. Vérifier les colonnes requises
    required_cols = {"date", "produit", "categorie", "quantite", "prix_unitaire", "ville"}
    cols_info = con.execute("PRAGMA table_info('ventes_raw')").fetchall()
    existing_cols = {col[1] for col in cols_info}
    
    missing_cols = required_cols - existing_cols
    if missing_cols:
        con.close()
        raise ValueError(f"Colonnes manquantes dans ventes_raw : {missing_cols}")
        
    # 3. Vérifier qu'il n'y a pas de valeurs nulles dans produit, quantite, ou prix_unitaire
    null_counts = con.execute("""
        SELECT 
            COUNT(CASE WHEN produit IS NULL THEN 1 END) as null_prod,
            COUNT(CASE WHEN quantite IS NULL THEN 1 END) as null_qty,
            COUNT(CASE WHEN prix_unitaire IS NULL THEN 1 END) as null_price
        FROM ventes_raw
    """).fetchone()
    
    con.close()
    
    if null_counts[0] > 0 or null_counts[1] > 0 or null_counts[2] > 0:
        raise ValueError(
            f"Valeurs nulles détectées dans les colonnes critiques. "
            f"Nulls produit: {null_counts[0]}, quantite: {null_counts[1]}, prix_unitaire: {null_counts[2]}"
        )
        
    print("Validation completed successfully! No critical null values found, all required columns exist.")

if __name__ == "__main__":
    validate_data()
