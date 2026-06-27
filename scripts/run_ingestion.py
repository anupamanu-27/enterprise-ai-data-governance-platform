from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from governance_platform.ingestion import ingest_marketing_campaigns


def main() -> None:
    result = ingest_marketing_campaigns(PROJECT_ROOT)
    print("Ingestion complete")
    print(f"Source file: {result.source_file}")
    print(f"Rows loaded: {result.row_count}")
    print(f"Postgres table: {result.postgres_table}")
    print(f"MinIO object: {result.minio_object}")


if __name__ == "__main__":
    main()

