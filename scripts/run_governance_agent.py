from __future__ import annotations

import argparse
import json

from governance_platform.agent import run_agent


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the AI governance agent.")
    parser.add_argument("question", help="Governance question.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of retrieved chunks.")
    parser.add_argument("--json", action="store_true", help="Print the full agent result as JSON.")
    args = parser.parse_args()

    result = run_agent(args.question, limit=args.limit)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"Intent: {result['intent']}")
    print()
    print("Actions:")
    for action in result["actions"]:
        print(f"- {action['name']}: {action['reason']}")
    print()
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
    print(f"Catalog assets available: {result['catalog_state']['asset_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
