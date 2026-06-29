from __future__ import annotations

import argparse
import json

from governance_platform.llm_answer import answer_governance_question


def main() -> int:
    parser = argparse.ArgumentParser(description="Answer a governance question with cited RAG context.")
    parser.add_argument("query", help="Governance question.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of retrieved chunks.")
    parser.add_argument("--json", action="store_true", help="Print full answer object as JSON.")
    args = parser.parse_args()

    result = answer_governance_question(args.query, limit=args.limit)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("Answer:")
    print(result["answer"])
    print()
    print("Citations:")
    for citation in result["citations"]:
        print(
            f"- [{citation['citation_id']}] "
            f"{citation['asset_id']} / {citation['chunk_id']} "
            f"(score={citation['score']})"
        )
    print()
    print(f"Model: {result['model']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
