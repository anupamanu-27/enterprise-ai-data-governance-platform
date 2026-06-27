from dataclasses import dataclass
import csv
from pathlib import Path
import subprocess


REQUIRED_CAMPAIGN_COLUMNS = (
    "campaign_id",
    "campaign_name",
    "channel",
    "region",
    "budget",
    "start_date",
    "end_date",
    "owner_name",
)


@dataclass(frozen=True)
class IngestionResult:
    source_file: Path
    row_count: int
    postgres_table: str
    minio_object: str


def read_campaign_rows(source_file: Path) -> list[dict[str, str]]:
    """Read and validate campaign rows from a CSV source file."""
    with source_file.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        missing_columns = set(REQUIRED_CAMPAIGN_COLUMNS) - set(reader.fieldnames or [])
        if missing_columns:
            columns = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns: {columns}")

        rows = list(reader)

    if not rows:
        raise ValueError("Campaign source file is empty")

    return rows


def build_campaign_insert_sql(rows: list[dict[str, str]]) -> str:
    """Build idempotent SQL for the raw marketing campaign table."""
    values = []
    for row in rows:
        values.append(
            "("
            f"{_sql_literal(row['campaign_id'])}, "
            f"{_sql_literal(row['campaign_name'])}, "
            f"{_sql_literal(row['channel'])}, "
            f"{_sql_literal(row['region'])}, "
            f"{row['budget']}, "
            f"{_sql_literal(row['start_date'])}, "
            f"{_sql_literal(row['end_date'])}, "
            f"{_sql_literal(row['owner_name'])}"
            ")"
        )

    values_sql = ",\n    ".join(values)

    return f"""
CREATE TABLE IF NOT EXISTS raw.marketing_campaigns (
    campaign_id VARCHAR(20) PRIMARY KEY,
    campaign_name VARCHAR(120) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    budget NUMERIC(12, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    owner_name VARCHAR(100) NOT NULL
);

INSERT INTO raw.marketing_campaigns (
    campaign_id,
    campaign_name,
    channel,
    region,
    budget,
    start_date,
    end_date,
    owner_name
) VALUES
    {values_sql}
ON CONFLICT (campaign_id) DO UPDATE SET
    campaign_name = EXCLUDED.campaign_name,
    channel = EXCLUDED.channel,
    region = EXCLUDED.region,
    budget = EXCLUDED.budget,
    start_date = EXCLUDED.start_date,
    end_date = EXCLUDED.end_date,
    owner_name = EXCLUDED.owner_name;
"""


def ingest_marketing_campaigns(project_root: Path) -> IngestionResult:
    """Load campaign data into Postgres and archive the raw file in MinIO."""
    source_file = project_root / "data" / "samples" / "marketing_campaigns.csv"
    rows = read_campaign_rows(source_file)
    sql = build_campaign_insert_sql(rows)

    _run_command(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "postgres",
            "psql",
            "-U",
            "governance_user",
            "-d",
            "governance_catalog",
            "-v",
            "ON_ERROR_STOP=1",
        ],
        cwd=project_root,
        input_text=sql,
    )

    minio_object = "raw/source/marketing_campaigns.csv"
    _run_command(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-T",
            "--volume",
            f"{source_file.resolve()}:/upload/marketing_campaigns.csv:ro",
            "minio-client",
            "mc alias set local http://minio:9000 \"$MINIO_ACCESS_KEY\" \"$MINIO_SECRET_KEY\"; "
            "mc cp /upload/marketing_campaigns.csv local/$MINIO_BUCKET_RAW/source/marketing_campaigns.csv; "
            "mc ls local/$MINIO_BUCKET_RAW/source/",
        ],
        cwd=project_root,
    )

    return IngestionResult(
        source_file=source_file,
        row_count=len(rows),
        postgres_table="raw.marketing_campaigns",
        minio_object=minio_object,
    )


def _sql_literal(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _run_command(
    command: list[str],
    cwd: Path,
    input_text: str | None = None,
) -> None:
    subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        text=True,
        check=True,
    )

