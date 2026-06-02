import os
import sys
from dagster import op, job

# Détermination des chemins absolus pour l'exécution des scripts et de dbt
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
DBT_DIR = os.path.join(os.path.dirname(PIPELINE_DIR), "dbt_pipeline")

@op
def ingest(context):
    script_path = os.path.join(PIPELINE_DIR, "ingest.py")
    context.log.info(f"Running ingestion script: {script_path}")
    exit_code = os.system(f'python "{script_path}"')
    if exit_code != 0:
        raise RuntimeError(f"Ingestion failed with exit code {exit_code}")

@op
def validate(context):
    script_path = os.path.join(PIPELINE_DIR, "validate.py")
    context.log.info(f"Running validation script: {script_path}")
    exit_code = os.system(f'python "{script_path}"')
    if exit_code != 0:
        raise RuntimeError(f"Validation failed with exit code {exit_code}")

@op
def transform(context):
    context.log.info("Running dbt models (dbt run)...")
    # Utilisation des variables d'environnement et de la ligne de commande dbt
    # --project-dir et --profiles-dir spécifient les chemins requis pour s'assurer que dbt s'exécute correctement
    exit_code = os.system(f'dbt run --project-dir "{DBT_DIR}" --profiles-dir "{DBT_DIR}"')
    if exit_code != 0:
        raise RuntimeError(f"dbt run failed with exit code {exit_code}")

@op
def test_data(context):
    context.log.info("Running dbt tests (dbt test)...")
    exit_code = os.system(f'dbt test --project-dir "{DBT_DIR}" --profiles-dir "{DBT_DIR}"')
    if exit_code != 0:
        raise RuntimeError(f"dbt test failed with exit code {exit_code}")

@job
def ventes_pipeline():
    # Enchaînement séquentiel des étapes
    ingest_result = ingest()
    validate_result = validate(ingest_result)
    transform_result = transform(validate_result)
    test_data(transform_result)
