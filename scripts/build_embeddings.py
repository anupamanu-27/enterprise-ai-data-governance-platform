from __future__ import annotations

from governance_platform.embeddings import build_embeddings


def main() -> int:
    output = build_embeddings()
    print(
        "Catalog embeddings built: "
        f"{output['chunk_count']} chunks, "
        f"{output['embedding_dimension']} dimensions"
    )
    print("Embeddings written to data/embeddings/catalog_embeddings.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
