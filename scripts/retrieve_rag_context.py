from __future__ import annotations

import argparse
import json

from governance_platform.rag import retrieve_for_rag


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve cited RAG context from Qdrant.")
    parser.add_argument("query", help="Governance question.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of retrieved chunks.")
    parser.add_argument("--json", action="store_true", help="Print the full retrieval object as JSON.")
    args = parser.parse_args()

    result = retrieve_for_rag(args.query, limit=args.limit)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"Query: {result['query']}")
    print(f"Retrieved chunks: {result['retrieval_count']}")
    print(f"Safety: {result['safety_note']}")
    print()
    print("Citations:")
    for citation in result["citations"]:
        print(
            f"- [{citation['citation_id']}] "
            f"{citation['asset_id']} / {citation['chunk_id']} "
            f"(score={citation['score']})"
        )
    print()
    print("Prompt preview:")
    print(result["prompt"][:1500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
