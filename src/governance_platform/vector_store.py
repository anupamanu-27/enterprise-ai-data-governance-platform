from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from governance_platform.embeddings import DEFAULT_EMBEDDINGS_PATH, EMBEDDING_DIMENSION, embed_text


DEFAULT_COLLECTION_NAME = "governance_catalog"


def qdrant_url() -> str:
    return os.getenv("QDRANT_URL", "http://localhost:6333").rstrip("/")


def point_id(chunk_id: str) -> int:
    digest = hashlib.sha256(chunk_id.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def request_json(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url=f"{qdrant_url()}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body) if response_body else {}


def recreate_collection(collection_name: str = DEFAULT_COLLECTION_NAME) -> None:
    try:
        request_json("DELETE", f"/collections/{collection_name}")
    except HTTPError as error:
        if error.code != 404:
            raise

    request_json(
        "PUT",
        f"/collections/{collection_name}",
        {
            "vectors": {
                "size": EMBEDDING_DIMENSION,
                "distance": "Cosine",
            }
        },
    )


def load_embedding_records(path: Path = DEFAULT_EMBEDDINGS_PATH) -> list[dict[str, Any]]:
    embeddings = json.loads(path.read_text(encoding="utf-8"))
    return embeddings["records"]


def record_to_point(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": point_id(record["chunk_id"]),
        "vector": record["embedding"],
        "payload": {
            "chunk_id": record["chunk_id"],
            "asset_id": record["asset_id"],
            "chunk_type": record["chunk_type"],
            "text": record["text"],
            "metadata": record["metadata"],
            "embedding_model": record["embedding_model"],
        },
    }


def upsert_embeddings(
    embeddings_path: Path = DEFAULT_EMBEDDINGS_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> dict[str, Any]:
    records = load_embedding_records(embeddings_path)
    recreate_collection(collection_name)
    points = [record_to_point(record) for record in records]
    request_json(
        "PUT",
        f"/collections/{collection_name}/points?wait=true",
        {"points": points},
    )
    return {
        "collection_name": collection_name,
        "point_count": len(points),
        "embedding_dimension": EMBEDDING_DIMENSION,
    }


def search_catalog(
    query: str,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    limit: int = 5,
) -> list[dict[str, Any]]:
    response = request_json(
        "POST",
        f"/collections/{collection_name}/points/query",
        {
            "query": embed_text(query),
            "limit": limit,
            "with_payload": True,
        },
    )
    return [
        {
            "score": result["score"],
            "chunk_id": result["payload"]["chunk_id"],
            "asset_id": result["payload"]["asset_id"],
            "chunk_type": result["payload"]["chunk_type"],
            "text": result["payload"]["text"],
            "metadata": result["payload"]["metadata"],
        }
        for result in response["result"]["points"]
    ]
