from __future__ import annotations

from datetime import datetime, timedelta
import csv
from pathlib import Path

from airflow.decorators import dag, task


WORKSPACE = Path("/workspace")
CAMPAIGN_SOURCE = WORKSPACE / "data" / "samples" / "marketing_campaigns.csv"
CURATED_CAMPAIGN_SUMMARY = WORKSPACE / "data" / "curated" / "campaign_summary"
ORCHESTRATION_SUMMARY = (
    WORKSPACE / "data" / "processed" / "airflow" / "governance_pipeline_summary.txt"
)

REQUIRED_CAMPAIGN_COLUMNS = {
    "campaign_id",
    "campaign_name",
    "channel",
    "region",
    "budget",
    "start_date",
    "end_date",
    "owner_name",
}


@dag(
    dag_id="governance_catalog_pipeline",
    description="Orchestrates checks for the AI data governance platform assets.",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "owner": "data-platform",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["governance", "catalog", "lesson-09"],
)
def governance_catalog_pipeline():
    @task
    def validate_campaign_source() -> int:
        if not CAMPAIGN_SOURCE.exists():
            raise FileNotFoundError(f"Missing source file: {CAMPAIGN_SOURCE}")

        with CAMPAIGN_SOURCE.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            missing_columns = REQUIRED_CAMPAIGN_COLUMNS - set(reader.fieldnames or [])
            if missing_columns:
                columns = ", ".join(sorted(missing_columns))
                raise ValueError(f"Campaign source is missing columns: {columns}")

            row_count = sum(1 for _ in reader)

        if row_count == 0:
            raise ValueError("Campaign source has no data rows")

        return row_count

    @task
    def validate_curated_campaign_summary() -> int:
        output_files = sorted(CURATED_CAMPAIGN_SUMMARY.glob("part-*.csv"))
        if not output_files:
            raise FileNotFoundError(
                f"Missing curated Spark output under {CURATED_CAMPAIGN_SUMMARY}"
            )

        with output_files[0].open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            row_count = sum(1 for _ in reader)

        if row_count == 0:
            raise ValueError("Curated campaign summary has no data rows")

        return row_count

    @task
    def publish_orchestration_summary(source_rows: int, curated_rows: int) -> str:
        ORCHESTRATION_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
        summary = (
            "Governance catalog pipeline completed.\n"
            f"Raw campaign rows checked: {source_rows}\n"
            f"Curated campaign summary rows checked: {curated_rows}\n"
        )
        ORCHESTRATION_SUMMARY.write_text(summary, encoding="utf-8")
        return str(ORCHESTRATION_SUMMARY)

    source_rows = validate_campaign_source()
    curated_rows = validate_curated_campaign_summary()
    publish_orchestration_summary(source_rows, curated_rows)


governance_catalog_pipeline()

