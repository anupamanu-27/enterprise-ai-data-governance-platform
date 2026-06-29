from __future__ import annotations

from governance_platform.vector_store import upsert_embeddings


def main() -> int:
    result = upsert_embeddings()
    print(
        "Loaded Qdrant collection "
        f"{result['collection_name']} with {result['point_count']} points"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
