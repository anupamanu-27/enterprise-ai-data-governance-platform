from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from governance_platform.catalog import DEFAULT_CATALOG_PATH, PROJECT_ROOT


DEFAULT_EMBEDDINGS_PATH = PROJECT_ROOT / "data" / "embeddings" / "catalog_embeddings.json"
EMBEDDING_DIMENSION = 64
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


@dataclass(frozen=True)
class CatalogChunk:
    chunk_id: str
    asset_id: str
    chunk_type: str
    text: str
    metadata: dict[str, Any]


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def stable_token_index(token: str, dimension: int = EMBEDDING_DIMENSION) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % dimension


def embed_text(text: str, dimension: int = EMBEDDING_DIMENSION) -> list[float]:
    vector = [0.0] * dimension
    for token in tokenize(text):
        vector[stable_token_index(token, dimension)] += 1.0

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector
    return [round(value / magnitude, 6) for value in vector]


def asset_text(asset: dict[str, Any]) -> str:
    pii_columns = ", ".join(column["name"] for column in asset["pii_summary"]["pii_columns"]) or "none"
    upstream_assets = ", ".join(asset["lineage"]["upstream_assets"]) or "none"
    downstream_assets = ", ".join(asset["lineage"]["downstream_assets"]) or "none"
    glossary_terms = ", ".join(term["term_name"] for term in asset["glossary_terms"]) or "none"

    return "\n".join(
        [
            f"Asset: {asset['qualified_name']}",
            f"Name: {asset['asset_name']}",
            f"Description: {asset['description']}",
            f"Owner: {asset['owner_name']}",
            f"Business domain: {asset['business_domain']}",
            f"Trust band: {asset['trust_band']}",
            f"Effective trust score: {asset['effective_trust_score']}",
            f"Contains PII: {asset['contains_pii']}",
            f"PII columns: {pii_columns}",
            f"Risk level: {asset['pii_summary']['risk_level']}",
            f"Upstream assets: {upstream_assets}",
            f"Downstream assets: {downstream_assets}",
            f"Glossary terms: {glossary_terms}",
        ]
    )


def column_text(asset: dict[str, Any], column: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Asset: {asset['qualified_name']}",
            f"Column: {column['name']}",
            f"Data type: {column['data_type']}",
            f"Nullable: {column['nullable']}",
            f"PII: {column['is_pii']}",
            f"PII type: {column['pii_type']}",
            f"Sensitivity: {column['sensitivity']}",
            f"Classification reason: {column['classification_reason']}",
        ]
    )


def build_catalog_chunks(catalog: dict[str, Any]) -> list[CatalogChunk]:
    chunks: list[CatalogChunk] = []
    for asset in catalog["assets"]:
        asset_id = asset["qualified_name"]
        chunks.append(
            CatalogChunk(
                chunk_id=f"{asset_id}::asset",
                asset_id=asset_id,
                chunk_type="asset_summary",
                text=asset_text(asset),
                metadata={
                    "asset_name": asset["asset_name"],
                    "owner_name": asset["owner_name"],
                    "business_domain": asset["business_domain"],
                    "trust_band": asset["trust_band"],
                    "contains_pii": asset["contains_pii"],
                    "risk_level": asset["pii_summary"]["risk_level"],
                },
            )
        )

        for column in asset["columns"]:
            chunks.append(
                CatalogChunk(
                    chunk_id=f"{asset_id}::column::{column['name']}",
                    asset_id=asset_id,
                    chunk_type="column_profile",
                    text=column_text(asset, column),
                    metadata={
                        "column_name": column["name"],
                        "data_type": column["data_type"],
                        "is_pii": column["is_pii"],
                        "pii_type": column["pii_type"],
                        "sensitivity": column["sensitivity"],
                    },
                )
            )

    return chunks


def chunk_to_record(chunk: CatalogChunk) -> dict[str, Any]:
    return {
        "chunk_id": chunk.chunk_id,
        "asset_id": chunk.asset_id,
        "chunk_type": chunk.chunk_type,
        "text": chunk.text,
        "metadata": chunk.metadata,
        "embedding_model": "local_hashing_embedding_v1",
        "embedding_dimension": EMBEDDING_DIMENSION,
        "embedding": embed_text(chunk.text),
    }


def build_embeddings(
    catalog_path: Path = DEFAULT_CATALOG_PATH,
    output_path: Path = DEFAULT_EMBEDDINGS_PATH,
) -> dict[str, Any]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    chunks = build_catalog_chunks(catalog)
    records = [chunk_to_record(chunk) for chunk in chunks]

    output = {
        "source_catalog": str(catalog_path),
        "embedding_model": "local_hashing_embedding_v1",
        "embedding_dimension": EMBEDDING_DIMENSION,
        "chunk_count": len(records),
        "records": records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    return output
