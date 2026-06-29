from __future__ import annotations

import argparse

from governance_platform.vector_store import search_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the governance catalog in Qdrant.")
    parser.add_argument("query", help="Question or search text.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results.")
    args = parser.parse_args()

    results = search_catalog(args.query, limit=args.limit)
    for index, result in enumerate(results, start=1):
        print(f"{index}. score={result['score']:.4f} asset={result['asset_id']}")
        print(f"   chunk={result['chunk_id']}")
        print(f"   type={result['chunk_type']}")
        print("   preview=" + result["text"].replace("\n", " | ")[:220])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
