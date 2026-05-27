# Main ETL script — fetch, transform, and load weather data into BigQuery

import sys
from logger import get_logger
from extract import fetch_all_cities
from transform import transform_all
from load import load_rows_to_bigquery

logger = get_logger(__name__)


def run_pipeline() -> None:
    """
    Orchestrates the full ETL pipeline:
    1. Extract — fetch raw weather data from Open-Meteo API
    2. Transform — flatten, clean, and enrich the data
    3. Load — upload transformed rows to BigQuery
    """
    logger.info("=== Weather ETL Pipeline started ===")

    # Step 1: Extract
    logger.info("Step 1/3 — Extracting data from Open-Meteo API")
    raw_data = fetch_all_cities()

    if not raw_data:
        logger.error("Extraction failed — no data returned for any city. Aborting pipeline.")
        sys.exit(1)

    logger.info(f"Extraction complete — {len(raw_data)} cities fetched")

    # Step 2: Transform
    logger.info("Step 2/3 — Transforming raw data")
    transformed_rows = transform_all(raw_data)

    if not transformed_rows:
        logger.error("Transformation produced no rows. Aborting pipeline.")
        sys.exit(1)

    logger.info(f"Transformation complete — {len(transformed_rows)} rows ready")

    # Step 3: Load
    logger.info("Step 3/3 — Loading data into BigQuery")
    success = load_rows_to_bigquery(transformed_rows)

    if not success:
        logger.error("Load step failed. Check logs above for details.")
        sys.exit(1)

    logger.info("=== Pipeline completed successfully ===")


if __name__ == "__main__":
    run_pipeline()