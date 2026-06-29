import unittest

from governance_platform.rag import (
    build_context_block,
    build_prompt,
    compact_text,
    make_citation,
    result_contains_pii,
)


class RagRetrievalTest(unittest.TestCase):
    def test_compact_text_removes_extra_lines(self):
        self.assertEqual(compact_text("Asset: raw.customers\n\nPII: True"), "Asset: raw.customers PII: True")

    def test_result_contains_pii_from_metadata(self):
        self.assertTrue(result_contains_pii({"metadata": {"is_pii": True}, "text": ""}))

    def test_result_contains_pii_from_text(self):
        self.assertTrue(result_contains_pii({"metadata": {}, "text": "Column: email\nPII: True"}))

    def test_make_citation_rounds_score(self):
        citation = make_citation(
            1,
            {
                "asset_id": "raw.customers",
                "chunk_id": "raw.customers::asset",
                "chunk_type": "asset_summary",
                "score": 0.123456,
            },
        )

        self.assertEqual(citation.citation_id, "C1")
        self.assertEqual(citation.score, 0.1235)

    def test_context_block_includes_citation_and_text(self):
        citation = make_citation(
            1,
            {
                "asset_id": "raw.customers",
                "chunk_id": "raw.customers::asset",
                "chunk_type": "asset_summary",
                "score": 0.9,
            },
        )
        block = build_context_block(
            citation,
            {
                "asset_id": "raw.customers",
                "chunk_id": "raw.customers::asset",
                "chunk_type": "asset_summary",
                "score": 0.9,
                "text": "Asset: raw.customers",
            },
        )

        self.assertIn("[C1]", block)
        self.assertIn("Asset: raw.customers", block)

    def test_build_prompt_requires_citations(self):
        prompt = build_prompt(
            query="Which tables contain PII?",
            context="[C1] Asset: raw.customers",
            safety_note="Retrieved context includes PII.",
        )

        self.assertIn("Cite sources", prompt)
        self.assertIn("Which tables contain PII?", prompt)
        self.assertIn("[C1]", prompt)


if __name__ == "__main__":
    unittest.main()
