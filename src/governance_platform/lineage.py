from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class LineageEdge:
    source_asset_id: str
    target_asset_id: str
    transformation_type: str
    description: str


LINEAGE_EDGES = [
    LineageEdge(
        source_asset_id="raw.customers",
        target_asset_id="analytics_staging.stg_customers",
        transformation_type="dbt_staging",
        description="Standardizes raw customer master data for analytics use.",
    ),
    LineageEdge(
        source_asset_id="raw.products",
        target_asset_id="analytics_staging.stg_products",
        transformation_type="dbt_staging",
        description="Standardizes raw product catalog data.",
    ),
    LineageEdge(
        source_asset_id="raw.sales_orders",
        target_asset_id="analytics_staging.stg_sales_orders",
        transformation_type="dbt_staging",
        description="Standardizes raw sales order transactions.",
    ),
    LineageEdge(
        source_asset_id="raw.support_tickets",
        target_asset_id="analytics_staging.stg_support_tickets",
        transformation_type="dbt_staging",
        description="Standardizes raw support case data.",
    ),
    LineageEdge(
        source_asset_id="raw.marketing_campaigns",
        target_asset_id="analytics_staging.stg_marketing_campaigns",
        transformation_type="dbt_staging",
        description="Standardizes campaign data loaded by the ingestion pipeline.",
    ),
    LineageEdge(
        source_asset_id="analytics_staging.stg_customers",
        target_asset_id="analytics_marts.mart_customer_revenue",
        transformation_type="dbt_mart",
        description="Adds customer identity and segmentation to revenue metrics.",
    ),
    LineageEdge(
        source_asset_id="analytics_staging.stg_sales_orders",
        target_asset_id="analytics_marts.mart_customer_revenue",
        transformation_type="dbt_mart",
        description="Aggregates order count, total revenue, and latest order date.",
    ),
    LineageEdge(
        source_asset_id="raw.customers",
        target_asset_id="analytics_marts.mart_customer_revenue",
        transformation_type="transitive_source",
        description="Customer identity flows through staging into the customer revenue mart.",
    ),
    LineageEdge(
        source_asset_id="raw.sales_orders",
        target_asset_id="analytics_marts.mart_customer_revenue",
        transformation_type="transitive_source",
        description="Sales transactions flow through staging into the customer revenue mart.",
    ),
    LineageEdge(
        source_asset_id="governance.data_assets",
        target_asset_id="analytics_marts.mart_governance_asset_health",
        transformation_type="dbt_mart",
        description="Turns governance ownership metadata into a trust-band mart.",
    ),
]


def edge_to_dict(edge: LineageEdge) -> dict[str, str]:
    return {
        "source_asset_id": edge.source_asset_id,
        "target_asset_id": edge.target_asset_id,
        "transformation_type": edge.transformation_type,
        "description": edge.description,
    }


def upstream_edges(asset_id: str) -> list[dict[str, str]]:
    return [edge_to_dict(edge) for edge in LINEAGE_EDGES if edge.target_asset_id == asset_id]


def downstream_edges(asset_id: str) -> list[dict[str, str]]:
    return [edge_to_dict(edge) for edge in LINEAGE_EDGES if edge.source_asset_id == asset_id]


def direct_upstreams(asset_id: str) -> list[str]:
    return sorted({edge.source_asset_id for edge in LINEAGE_EDGES if edge.target_asset_id == asset_id})


def direct_downstreams(asset_id: str) -> list[str]:
    return sorted({edge.target_asset_id for edge in LINEAGE_EDGES if edge.source_asset_id == asset_id})


def transitive_upstreams(asset_id: str) -> list[str]:
    visited: set[str] = set()
    queue = deque(direct_upstreams(asset_id))

    while queue:
        current_asset_id = queue.popleft()
        if current_asset_id in visited:
            continue
        visited.add(current_asset_id)
        queue.extend(direct_upstreams(current_asset_id))

    return sorted(visited)


def lineage_summary(asset_id: str) -> dict:
    return {
        "upstream_assets": direct_upstreams(asset_id),
        "downstream_assets": direct_downstreams(asset_id),
        "all_upstream_assets": transitive_upstreams(asset_id),
        "upstream_edges": upstream_edges(asset_id),
        "downstream_edges": downstream_edges(asset_id),
    }


def lineage_graph() -> dict:
    nodes = sorted(
        {
            edge.source_asset_id
            for edge in LINEAGE_EDGES
        }
        | {
            edge.target_asset_id
            for edge in LINEAGE_EDGES
        }
    )
    return {
        "node_count": len(nodes),
        "edge_count": len(LINEAGE_EDGES),
        "nodes": nodes,
        "edges": [edge_to_dict(edge) for edge in LINEAGE_EDGES],
    }
