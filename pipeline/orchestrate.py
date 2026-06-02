import os
import sys
from dagster import op, job, In, Nothing

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

@op(ins={"start": In(Nothing)})
def validate(context):
    script_path = os.path.join(PIPELINE_DIR, "validate.py")
    context.log.info(f"Running validation script: {script_path}")
    exit_code = os.system(f'python "{script_path}"')
    if exit_code != 0:
        raise RuntimeError(f"Validation failed with exit code {exit_code}")

@op(ins={"start": In(Nothing)})
def transform(context):
    context.log.info("Running dbt models (dbt run)...")
    # Se déplacer dans le dossier dbt_pipeline pour que le chemin relatif ../ventes.duckdb soit résolu correctement
    exit_code = os.system(f'cd /d "{DBT_DIR}" && dbt run --project-dir "{DBT_DIR}" --profiles-dir "{DBT_DIR}"')
    if exit_code != 0:
        raise RuntimeError(f"dbt run failed with exit code {exit_code}")

@op(ins={"start": In(Nothing)})
def test_data(context):
    context.log.info("Running dbt tests (dbt test)...")
    # Se déplacer dans le dossier dbt_pipeline pour que le chemin relatif ../ventes.duckdb soit résolu correctement
    exit_code = os.system(f'cd /d "{DBT_DIR}" && dbt test --project-dir "{DBT_DIR}" --profiles-dir "{DBT_DIR}"')
    if exit_code != 0:
        raise RuntimeError(f"dbt test failed with exit code {exit_code}")

@job
def ventes_pipeline():
    # Enchaînement séquentiel en passant le résultat (représentant le signal de fin de l'op précédente)
    ingest_result = ingest()
    validate_result = validate(start=ingest_result)
    transform_result = transform(start=validate_result)
    test_data(start=transform_result)

