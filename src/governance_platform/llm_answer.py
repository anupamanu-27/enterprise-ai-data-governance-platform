from __future__ import annotations

import re
from typing import Any

from governance_platform.rag import retrieve_for_rag


ASSET_PATTERN = re.compile(r"asset=([^;]+);")
COLUMN_PATTERN = re.compile(r"Column: ([^ ]+)")
PII_TYPE_PATTERN = re.compile(r"PII type: ([^ ]+)")
TRUST_BAND_PATTERN = re.compile(r"Trust band: ([^ ]+)")
OWNER_PATTERN = re.compile(r"Owner: ([^|]+?)(?: Business domain:|$)")
UPSTREAM_PATTERN = re.compile(r"Upstream assets: ([^|]+)")


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values = []
    for value in values:
        clean_value = value.strip()
        if clean_value and clean_value not in seen:
            seen.add(clean_value)
            unique_values.append(clean_value)
    return unique_values


def citation_lookup(rag_result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {citation["citation_id"]: citation for citation in rag_result["citations"]}


def extract_cited_facts(rag_result: dict[str, Any]) -> list[dict[str, str]]:
    facts = []
    for block in rag_result["context"].split("\n\n"):
        if not block.strip():
            continue
        citation_id = block.split("]", 1)[0].replace("[", "")
        asset_match = ASSET_PATTERN.search(block)
        column_match = COLUMN_PATTERN.search(block)
        pii_type_match = PII_TYPE_PATTERN.search(block)
        trust_band_match = TRUST_BAND_PATTERN.search(block)
        owner_match = OWNER_PATTERN.search(block)
        upstream_match = UPSTREAM_PATTERN.search(block)

        facts.append(
            {
                "citation_id": citation_id,
                "asset_id": asset_match.group(1).strip() if asset_match else "",
                "column_name": column_match.group(1).strip() if column_match else "",
                "pii_type": pii_type_match.group(1).strip() if pii_type_match else "",
                "trust_band": trust_band_match.group(1).strip() if trust_band_match else "",
                "owner_name": owner_match.group(1).strip() if owner_match else "",
                "upstream_assets": upstream_match.group(1).strip() if upstream_match else "",
            }
        )
    return facts


def answer_pii_question(facts: list[dict[str, str]]) -> str:
    pii_facts = [fact for fact in facts if fact["column_name"] and fact["pii_type"] not in {"", "None"}]
    if not pii_facts:
        return "I found retrieved context, but it did not clearly identify PII columns."

    grouped: dict[str, list[str]] = {}
    citation_ids: dict[str, list[str]] = {}
    for fact in pii_facts:
        grouped.setdefault(fact["asset_id"], []).append(f"{fact['column_name']} ({fact['pii_type']})")
        citation_ids.setdefault(fact["asset_id"], []).append(f"[{fact['citation_id']}]")

    lines = ["The retrieved catalog context shows these assets contain customer-related PII:"]
    for asset_id, columns in grouped.items():
        lines.append(
            f"- {asset_id}: {', '.join(unique_preserve_order(columns))} "
            f"{' '.join(unique_preserve_order(citation_ids[asset_id]))}"
        )
    return "\n".join(lines)


def answer_lineage_question(facts: list[dict[str, str]]) -> str:
    lineage_facts = [fact for fact in facts if fact["upstream_assets"] and fact["upstream_assets"] != "none"]
    if not lineage_facts:
        return "I found retrieved context, but it did not clearly include upstream lineage."

    lines = ["The retrieved catalog context shows this lineage:"]
    for fact in lineage_facts:
        lines.append(f"- {fact['asset_id']} is fed by {fact['upstream_assets']} [{fact['citation_id']}]")
    return "\n".join(lines)


def answer_general_question(facts: list[dict[str, str]]) -> str:
    if not facts:
        return "I could not find enough retrieved catalog context to answer this question."

    cited_assets = unique_preserve_order([fact["asset_id"] for fact in facts if fact["asset_id"]])
    citations = unique_preserve_order([f"[{fact['citation_id']}]" for fact in facts if fact["citation_id"]])
    return (
        "The retrieved governance context is most relevant to these assets: "
        f"{', '.join(cited_assets)}. Sources: {' '.join(citations)}"
    )


def draft_answer(query: str, rag_result: dict[str, Any]) -> str:
    facts = extract_cited_facts(rag_result)
    normalized_query = query.lower()

    if "pii" in normalized_query or "sensitive" in normalized_query:
        answer = answer_pii_question(facts)
    elif "lineage" in normalized_query or "upstream" in normalized_query or "feed" in normalized_query:
        answer = answer_lineage_question(facts)
    else:
        answer = answer_general_question(facts)

    return "\n\n".join(
        [
            answer,
            f"Safety note: {rag_result['safety_note']}",
            "This answer was generated from retrieved catalog context only.",
        ]
    )


def answer_governance_question(query: str, limit: int = 5) -> dict[str, Any]:
    rag_result = retrieve_for_rag(query, limit=limit)
    return {
        "query": query,
        "answer": draft_answer(query, rag_result),
        "citations": rag_result["citations"],
        "retrieval_count": rag_result["retrieval_count"],
        "pii_detected_in_context": rag_result["pii_detected_in_context"],
        "model": "local_citation_synthesizer_v1",
        "prompt": rag_result["prompt"],
    }
