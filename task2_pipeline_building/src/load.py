# Data loading — upload transformed weather data to BigQuery

from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
from typing import Optional
from logger import get_logger
from config import (
    GCP_PROJECT_ID,
    BIGQUERY_DATASET,
    BIGQUERY_TABLE,
    BIGQUERY_TABLE_ID,
    BIGQUERY_LOCATION,
    BIGQUERY_WRITE_DISPOSITION,
)

logger = get_logger(__name__)

# BigQuery schema matching the transformed row structure
BIGQUERY_SCHEMA = [
    bigquery.SchemaField("city", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("temperature_max", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("temperature_min", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("precipitation", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("uv_index", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("windspeed_max", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("humidity", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("weather_category", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("heatwave_flag", "BOOL", mode="NULLABLE"),
    bigquery.SchemaField("uv_risk_level", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("campaign_condition_score", "FLOAT", mode="NULLABLE"),
]


def get_bigquery_client() -> Optional[bigquery.Client]:
    """
    Initialises and returns a BigQuery client.
    Returns None if initialisation fails.
    """
    try:
        client = bigquery.Client(
            project=GCP_PROJECT_ID,
            location=BIGQUERY_LOCATION,
        )
        logger.info(f"BigQuery client initialised for project: {GCP_PROJECT_ID}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialise BigQuery client: {e}")
        return None


def ensure_table_exists(client: bigquery.Client) -> bool:
    """
    Creates the BigQuery table if it does not already exist.
    Returns True if table is ready, False if creation failed.
    """
    dataset_ref = bigquery.DatasetReference(GCP_PROJECT_ID, BIGQUERY_DATASET)
    table_ref = dataset_ref.table(BIGQUERY_TABLE)

    try:
        client.get_table(table_ref)
        logger.info(f"Table {BIGQUERY_TABLE_ID} already exists")
        return True

    except Exception:
        # Table does not exist — create it
        logger.info(f"Table {BIGQUERY_TABLE_ID} not found — creating it")
        table = bigquery.Table(table_ref, schema=BIGQUERY_SCHEMA)

        try:
            client.create_table(table)
            logger.info(f"Table {BIGQUERY_TABLE_ID} created successfully")
            return True
        except GoogleAPIError as e:
            logger.error(f"Failed to create table {BIGQUERY_TABLE_ID}: {e}")
            return False


def load_rows_to_bigquery(rows: list[dict]) -> bool:
    """
    Uploads a list of transformed row dicts to BigQuery.
    Returns True if load was successful, False otherwise.
    """
    if not rows:
        logger.warning("No rows to load — skipping BigQuery upload")
        return False

    client = get_bigquery_client()
    if client is None:
        return False

    table_ready = ensure_table_exists(client)
    if not table_ready:
        return False

    job_config = bigquery.LoadJobConfig(
        schema=BIGQUERY_SCHEMA,
        write_disposition=BIGQUERY_WRITE_DISPOSITION,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    logger.info(f"Loading {len(rows)} rows into {BIGQUERY_TABLE_ID}")

    try:
        load_job = client.load_table_from_json(
            rows,
            BIGQUERY_TABLE_ID,
            job_config=job_config,
        )

        # Wait for the job to complete
        load_job.result()

        if load_job.errors:
            logger.error(f"BigQuery load job completed with errors: {load_job.errors}")
            return False

        logger.info(f"Successfully loaded {len(rows)} rows into {BIGQUERY_TABLE_ID}")
        return True

    except GoogleAPIError as e:
        logger.error(f"BigQuery API error during load: {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during BigQuery load: {e}")
        return False