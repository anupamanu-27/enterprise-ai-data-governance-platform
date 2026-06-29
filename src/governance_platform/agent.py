from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from governance_platform.catalog import DEFAULT_CATALOG_PATH
from governance_platform.llm_answer import answer_governance_question


@dataclass(frozen=True)
class AgentAction:
    name: str
    reason: str


def classify_intent(question: str) -> str:
    normalized_question = question.lower()
    if any(keyword in normalized_question for keyword in ["pii", "sensitive", "privacy"]):
        return "pii_check"
    if any(keyword in normalized_question for keyword in ["lineage", "upstream", "downstream", "feed", "impact"]):
        return "lineage_check"
    if any(keyword in normalized_question for keyword in ["owner", "owns", "trust", "quality", "domain"]):
        return "catalog_lookup"
    return "general_governance_answer"


def plan_actions(intent: str) -> list[AgentAction]:
    if intent == "pii_check":
        return [
            AgentAction("search_catalog", "Find catalog chunks related to sensitive or personal data."),
            AgentAction("answer_with_citations", "Summarize PII findings with source citations."),
            AgentAction("add_safety_note", "Warn that retrieved context contains sensitive metadata."),
        ]

    if intent == "lineage_check":
        return [
            AgentAction("search_catalog", "Find lineage-aware catalog chunks."),
            AgentAction("answer_with_citations", "Explain upstream or downstream relationships with citations."),
        ]

    if intent == "catalog_lookup":
        return [
            AgentAction("search_catalog", "Find owner, domain, trust, or quality metadata."),
            AgentAction("answer_with_citations", "Summarize catalog metadata with citations."),
        ]

    return [
        AgentAction("search_catalog", "Find relevant governance catalog context."),
        AgentAction("answer_with_citations", "Generate a cited answer from retrieved context."),
    ]


def load_catalog(path: Path = DEFAULT_CATALOG_PATH) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_catalog_state(catalog: dict[str, Any] | None) -> dict[str, Any]:
    if catalog is None:
        return {
            "catalog_available": False,
            "asset_count": 0,
            "high_risk_assets": [],
        }

    high_risk_assets = [
        asset["qualified_name"]
        for asset in catalog["assets"]
        if asset["pii_summary"]["risk_level"] in {"high", "restricted"}
    ]
    return {
        "catalog_available": True,
        "asset_count": catalog["asset_count"],
        "high_risk_assets": high_risk_assets,
    }


def run_agent(question: str, limit: int = 5) -> dict[str, Any]:
    intent = classify_intent(question)
    actions = plan_actions(intent)
    answer = answer_governance_question(question, limit=limit)
    catalog_state = summarize_catalog_state(load_catalog())

    return {
        "question": question,
        "intent": intent,
        "actions": [
            {
                "name": action.name,
                "reason": action.reason,
            }
            for action in actions
        ],
        "answer": answer["answer"],
        "citations": answer["citations"],
        "model": answer["model"],
        "retrieval_count": answer["retrieval_count"],
        "pii_detected_in_context": answer["pii_detected_in_context"],
        "catalog_state": catalog_state,
    }
