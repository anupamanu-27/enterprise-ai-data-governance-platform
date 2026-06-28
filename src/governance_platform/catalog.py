from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import psycopg2
import psycopg2.extras

from governance_platform.pii import classify_columns, summarize_pii


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUALITY_REPORT_PATH = PROJECT_ROOT / "quality" / "reports" / "latest_quality_report.json"
DEFAULT_CATALOG_PATH = PROJECT_ROOT / "data" / "catalog" / "metadata_catalog.json"
DISCOVERED_SCHEMAS = ("raw", "analytics_marts")


@dataclass(frozen=True)
class CatalogAsset:
    asset_id: str
    asset_name: str
    schema_name: str
    table_name: str
    asset_type: str
    owner_name: str
    business_domain: str
    contains_pii: bool
    base_trust_score: int
    description: str


def connection_settings() -> dict[str, str]:
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "dbname": os.getenv("POSTGRES_DB", "governance_catalog"),
        "user": os.getenv("POSTGRES_USER", "governance_user"),
        "password": os.getenv("POSTGRES_PASSWORD", "change_me"),
    }


def display_name(table_name: str) -> str:
    return table_name.replace("_", " ").title()


def default_asset_metadata(schema_name: str, table_name: str) -> CatalogAsset:
    asset_id = f"{schema_name}.{table_name}"
    business_domain = "Analytics" if schema_name == "analytics_marts" else "Source Data"
    trust_score = 90 if schema_name == "analytics_marts" else 70
    return CatalogAsset(
        asset_id=asset_id,
        asset_name=display_name(table_name),
        schema_name=schema_name,
        table_name=table_name,
        asset_type="table",
        owner_name="Data Platform Team",
        business_domain=business_domain,
        contains_pii=False,
        base_trust_score=trust_score,
        description=f"Discovered {schema_name} table used by the governance platform.",
    )


def load_quality_report(path: Path = DEFAULT_QUALITY_REPORT_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"overall_success": None, "assets": []}
    return json.loads(path.read_text(encoding="utf-8"))


def quality_by_asset(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        asset["qualified_name"]: {
            "success": asset["success"],
            "row_count": asset["row_count"],
            "passed_checks": asset["passed_checks"],
            "failed_checks": asset["failed_checks"],
            "total_checks": asset["total_checks"],
        }
        for asset in report.get("assets", [])
    }


def calculate_effective_trust_score(base_score: int, quality_summary: dict[str, Any] | None) -> int:
    if quality_summary is None:
        return base_score
    penalty = int(quality_summary["failed_checks"]) * 10
    bonus = 5 if quality_summary["success"] else 0
    return max(0, min(100, base_score + bonus - penalty))


def trust_band(score: int) -> str:
    if score >= 85:
        return "high_trust"
    if score >= 70:
        return "medium_trust"
    return "needs_attention"


def fetch_discovered_tables(connection: Any) -> list[dict[str, str]]:
    with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(
            """
            select table_schema, table_name, table_type
            from information_schema.tables
            where table_schema = any(%s)
            order by table_schema, table_name
            """,
            (list(DISCOVERED_SCHEMAS),),
        )
        return list(cursor.fetchall())


def fetch_columns(connection: Any) -> dict[str, list[dict[str, Any]]]:
    with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(
            """
            select
                table_schema,
                table_name,
                column_name,
                data_type,
                ordinal_position,
                is_nullable
            from information_schema.columns
            where table_schema = any(%s)
            order by table_schema, table_name, ordinal_position
            """,
            (list(DISCOVERED_SCHEMAS),),
        )
        rows = cursor.fetchall()

    columns_by_asset: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        asset_id = f"{row['table_schema']}.{row['table_name']}"
        columns_by_asset.setdefault(asset_id, []).append(
            {
                "name": row["column_name"],
                "data_type": row["data_type"],
                "ordinal_position": row["ordinal_position"],
                "nullable": row["is_nullable"] == "YES",
            }
        )
    return columns_by_asset


def fetch_governed_assets(connection: Any) -> dict[str, CatalogAsset]:
    with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(
            """
            select
                asset_id,
                asset_name,
                schema_name,
                split_part(asset_id, '.', 2) as table_name,
                asset_type,
                owner_name,
                business_domain,
                contains_pii,
                trust_score,
                description
            from governance.data_assets
            """
        )
        rows = cursor.fetchall()

    return {
        row["asset_id"]: CatalogAsset(
            asset_id=row["asset_id"],
            asset_name=row["asset_name"],
            schema_name=row["schema_name"],
            table_name=row["table_name"],
            asset_type=row["asset_type"],
            owner_name=row["owner_name"],
            business_domain=row["business_domain"],
            contains_pii=row["contains_pii"],
            base_trust_score=row["trust_score"],
            description=row["description"],
        )
        for row in rows
    }


def fetch_glossary_terms(connection: Any) -> dict[str, list[dict[str, str]]]:
    with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(
            """
            select term_id, term_name, definition, owner_name, related_asset_id
            from governance.business_glossary
            order by term_name
            """
        )
        rows = cursor.fetchall()

    terms_by_asset: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        terms_by_asset.setdefault(row["related_asset_id"], []).append(
            {
                "term_id": row["term_id"],
                "term_name": row["term_name"],
                "definition": row["definition"],
                "owner_name": row["owner_name"],
            }
        )
    return terms_by_asset


def build_catalog(report_path: Path = DEFAULT_QUALITY_REPORT_PATH) -> dict[str, Any]:
    quality_report = load_quality_report(report_path)
    quality_lookup = quality_by_asset(quality_report)

    with psycopg2.connect(**connection_settings()) as connection:
        discovered_tables = fetch_discovered_tables(connection)
        columns_by_asset = fetch_columns(connection)
        governed_assets = fetch_governed_assets(connection)
        glossary_terms = fetch_glossary_terms(connection)

    catalog_assets = []
    for table in discovered_tables:
        schema_name = table["table_schema"]
        table_name = table["table_name"]
        asset_id = f"{schema_name}.{table_name}"
        metadata = governed_assets.get(asset_id, default_asset_metadata(schema_name, table_name))
        quality_summary = quality_lookup.get(asset_id)
        effective_score = calculate_effective_trust_score(metadata.base_trust_score, quality_summary)
        classified_columns = classify_columns(columns_by_asset.get(asset_id, []))
        pii_summary = summarize_pii(classified_columns)

        catalog_assets.append(
            {
                "asset_id": metadata.asset_id,
                "asset_name": metadata.asset_name,
                "qualified_name": asset_id,
                "schema_name": schema_name,
                "table_name": table_name,
                "asset_type": metadata.asset_type,
                "owner_name": metadata.owner_name,
                "business_domain": metadata.business_domain,
                "contains_pii": metadata.contains_pii or pii_summary["contains_pii"],
                "description": metadata.description,
                "base_trust_score": metadata.base_trust_score,
                "effective_trust_score": effective_score,
                "trust_band": trust_band(effective_score),
                "pii_summary": pii_summary,
                "quality": quality_summary,
                "columns": classified_columns,
                "glossary_terms": glossary_terms.get(asset_id, []),
            }
        )

    return {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "asset_count": len(catalog_assets),
        "quality_report_available": quality_report.get("overall_success") is not None,
        "assets": catalog_assets,
    }


def write_catalog(catalog_path: Path = DEFAULT_CATALOG_PATH) -> dict[str, Any]:
    catalog = build_catalog()
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    return catalog
