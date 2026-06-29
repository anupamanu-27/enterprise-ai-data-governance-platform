import unittest

from governance_platform.agent import classify_intent, plan_actions, summarize_catalog_state


class AgentTest(unittest.TestCase):
    def test_classify_pii_intent(self):
        self.assertEqual(classify_intent("Which tables contain PII?"), "pii_check")

    def test_classify_lineage_intent(self):
        self.assertEqual(classify_intent("What feeds customer revenue?"), "lineage_check")

    def test_classify_catalog_lookup_intent(self):
        self.assertEqual(classify_intent("Who owns the customer table?"), "catalog_lookup")

    def test_plan_pii_actions_includes_safety_note(self):
        action_names = [action.name for action in plan_actions("pii_check")]

        self.assertIn("search_catalog", action_names)
        self.assertIn("answer_with_citations", action_names)
        self.assertIn("add_safety_note", action_names)

    def test_catalog_state_lists_high_risk_assets(self):
        state = summarize_catalog_state(
            {
                "asset_count": 2,
                "assets": [
                    {
                        "qualified_name": "raw.customers",
                        "pii_summary": {"risk_level": "high"},
                    },
                    {
                        "qualified_name": "raw.products",
                        "pii_summary": {"risk_level": "low"},
                    },
                ],
            }
        )

        self.assertTrue(state["catalog_available"])
        self.assertEqual(state["high_risk_assets"], ["raw.customers"])


if __name__ == "__main__":
    unittest.main()
