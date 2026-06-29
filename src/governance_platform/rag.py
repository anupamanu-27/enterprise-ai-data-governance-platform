from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from governance_platform.vector_store import search_catalog


@dataclass(frozen=True)
class Citation:
    citation_id: str
    asset_id: str
    chunk_id: str
    chunk_type: str
    score: float


def compact_text(text: str) -> str:
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def result_contains_pii(result: dict[str, Any]) -> bool:
    metadata = result.get("metadata", {})
    if metadata.get("contains_pii") is True:
        return True
    if metadata.get("is_pii") is True:
        return True
    return "PII: True" in result.get("text", "")


def make_citation(index: int, result: dict[str, Any]) -> Citation:
    return Citation(
        citation_id=f"C{index}",
        asset_id=result["asset_id"],
        chunk_id=result["chunk_id"],
        chunk_type=result["chunk_type"],
        score=round(float(result["score"]), 4),
    )


def build_context_block(citation: Citation, result: dict[str, Any]) -> str:
    preview = compact_text(result["text"])
    return (
        f"[{citation.citation_id}] "
        f"asset={citation.asset_id}; "
        f"chunk={citation.chunk_id}; "
        f"type={citation.chunk_type}; "
        f"score={citation.score}\n"
        f"{preview}"
    )


def build_rag_context(query: str, limit: int = 5) -> dict[str, Any]:
    results = search_catalog(query, limit=limit)
    citations = [make_citation(index, result) for index, result in enumerate(results, start=1)]
    context_blocks = [
        build_context_block(citation, result)
        for citation, result in zip(citations, results, strict=True)
    ]
    pii_detected = any(result_contains_pii(result) for result in results)

    return {
        "query": query,
        "retrieval_count": len(results),
        "pii_detected_in_context": pii_detected,
        "safety_note": (
            "Retrieved context includes PII or sensitive data. Do not expose raw values to an LLM response."
            if pii_detected
            else "No PII was detected in the retrieved context metadata."
        ),
        "context": "\n\n".join(context_blocks),
        "citations": [
            {
                "citation_id": citation.citation_id,
                "asset_id": citation.asset_id,
                "chunk_id": citation.chunk_id,
                "chunk_type": citation.chunk_type,
                "score": citation.score,
            }
            for citation in citations
        ],
    }


def build_prompt(query: str, context: str, safety_note: str) -> str:
    return "\n".join(
        [
            "You are an enterprise data governance assistant.",
            "Answer using only the provided context.",
            "Cite sources using citation IDs like [C1].",
            "If the context is insufficient, say what is missing.",
            f"Safety note: {safety_note}",
            "",
            f"Question: {query}",
            "",
            "Context:",
            context,
        ]
    )


def retrieve_for_rag(query: str, limit: int = 5) -> dict[str, Any]:
    rag_context = build_rag_context(query, limit=limit)
    rag_context["prompt"] = build_prompt(
        query=rag_context["query"],
        context=rag_context["context"],
        safety_note=rag_context["safety_note"],
    )
    return rag_context
