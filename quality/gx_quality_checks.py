from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import great_expectations as gx
import pandas as pd
import psycopg2


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = PROJECT_ROOT / "quality" / "reports" / "latest_quality_report.json"


@dataclass(frozen=True)
class QualityAsset:
    name: str
    schema_name: str
    table_name: str

    @property
    def qualified_name(self) -> str:
        return f"{self.schema_name}.{self.table_name}"


QUALITY_ASSETS = [
    QualityAsset(
        name="customer_revenue_mart",
        schema_name="analytics_marts",
        table_name="mart_customer_revenue",
    ),
    QualityAsset(
        name="governance_asset_health_mart",
        schema_name="analytics_marts",
        table_name="mart_governance_asset_health",
    ),
]


def connection_settings() -> dict[str, str]:
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "dbname": os.getenv("POSTGRES_DB", "governance_catalog"),
        "user": os.getenv("POSTGRES_USER", "governance_user"),
        "password": os.getenv("POSTGRES_PASSWORD", "change_me"),
    }


def load_asset_dataframe(asset: QualityAsset) -> pd.DataFrame:
    query = f"select * from {asset.qualified_name}"
    with psycopg2.connect(**connection_settings()) as connection:
        return pd.read_sql_query(query, connection)


def expectations_for(asset: QualityAsset) -> list[Any]:
    if asset.name == "customer_revenue_mart":
        return [
            gx.expectations.ExpectTableRowCountToBeBetween(min_value=1, max_value=1000),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"),
            gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id"),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="full_name"),
            gx.expectations.ExpectColumnValuesToBeBetween(column="total_revenue", min_value=0),
            gx.expectations.ExpectColumnValuesToBeBetween(column="order_count", min_value=1),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="segment",
                value_set=["Enterprise", "Mid-Market", "SMB"],
            ),
        ]

    if asset.name == "governance_asset_health_mart":
        return [
            gx.expectations.ExpectTableRowCountToBeBetween(min_value=1, max_value=1000),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="asset_id"),
            gx.expectations.ExpectColumnValuesToBeUnique(column="asset_id"),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="owner_name"),
            gx.expectations.ExpectColumnValuesToBeBetween(column="trust_score", min_value=0, max_value=100),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="trust_band",
                value_set=["high_trust", "medium_trust", "needs_attention"],
            ),
        ]

    raise ValueError(f"No expectations configured for asset: {asset.name}")


def to_json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: to_json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_json_safe(item) for item in value]
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def validate_asset(context: Any, asset: QualityAsset) -> dict[str, Any]:
    dataframe = load_asset_dataframe(asset)
    data_source = context.data_sources.add_pandas(f"{asset.name}_source")
    dataframe_asset = data_source.add_dataframe_asset(name=asset.name)
    batch_definition = dataframe_asset.add_batch_definition_whole_dataframe("full_table")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": dataframe})

    checks = []
    for expectation in expectations_for(asset):
        result = batch.validate(expectation)
        checks.append(
            {
                "expectation": result.expectation_config.type,
                "success": bool(result.success),
                "result": to_json_safe(result.result),
            }
        )

    passed_checks = sum(1 for check in checks if check["success"])
    total_checks = len(checks)

    return {
        "asset_name": asset.name,
        "qualified_name": asset.qualified_name,
        "row_count": int(len(dataframe)),
        "success": passed_checks == total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "total_checks": total_checks,
        "checks": checks,
    }


def run_quality_checks(report_path: Path = DEFAULT_REPORT_PATH) -> dict[str, Any]:
    context = gx.get_context(mode="ephemeral")
    asset_results = [validate_asset(context, asset) for asset in QUALITY_ASSETS]
    passed_assets = sum(1 for result in asset_results if result["success"])
    total_checks = sum(result["total_checks"] for result in asset_results)
    failed_checks = sum(result["failed_checks"] for result in asset_results)

    report = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "tool": "great_expectations",
        "overall_success": failed_checks == 0,
        "asset_count": len(asset_results),
        "passed_assets": passed_assets,
        "failed_assets": len(asset_results) - passed_assets,
        "total_checks": total_checks,
        "failed_checks": failed_checks,
        "assets": asset_results,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

