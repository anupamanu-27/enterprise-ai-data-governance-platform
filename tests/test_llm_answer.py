import unittest

from governance_platform.llm_answer import (
    draft_answer,
    extract_cited_facts,
    unique_preserve_order,
)


class LlmAnswerTest(unittest.TestCase):
    def test_unique_preserve_order(self):
        self.assertEqual(unique_preserve_order(["a", "b", "a"]), ["a", "b"])

    def test_extract_cited_facts_reads_column_and_pii_type(self):
        result = {
            "context": (
                "[C1] asset=raw.customers; chunk=raw.customers::column::email; "
                "type=column_profile; score=0.5\n"
                "Asset: raw.customers Column: email PII: True PII type: email"
            ),
            "citations": [],
        }

        facts = extract_cited_facts(result)

        self.assertEqual(facts[0]["citation_id"], "C1")
        self.assertEqual(facts[0]["asset_id"], "raw.customers")
        self.assertEqual(facts[0]["column_name"], "email")
        self.assertEqual(facts[0]["pii_type"], "email")

    def test_draft_answer_for_pii_question_uses_citations(self):
        rag_result = {
            "context": (
                "[C1] asset=raw.customers; chunk=raw.customers::column::email; "
                "type=column_profile; score=0.5\n"
                "Asset: raw.customers Column: email PII: True PII type: email"
            ),
            "citations": [{"citation_id": "C1"}],
            "safety_note": "Retrieved context includes PII.",
        }

        answer = draft_answer("Which tables contain PII?", rag_result)

        self.assertIn("raw.customers", answer)
        self.assertIn("email", answer)
        self.assertIn("[C1]", answer)

    def test_draft_answer_for_general_question_lists_assets(self):
        rag_result = {
            "context": "[C1] asset=raw.customers; chunk=raw.customers::asset; type=asset_summary; score=0.5\nAsset: raw.customers",
            "citations": [{"citation_id": "C1"}],
            "safety_note": "No PII was detected.",
        }

        answer = draft_answer("Tell me about customers", rag_result)

        self.assertIn("raw.customers", answer)
        self.assertIn("[C1]", answer)


if __name__ == "__main__":
    unittest.main()
