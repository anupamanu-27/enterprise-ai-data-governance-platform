import unittest

from governance_platform.pii import classify_column, classify_columns, summarize_pii


class PiiClassificationTest(unittest.TestCase):
    def test_email_column_is_high_risk_pii(self):
        result = classify_column("email")

        self.assertTrue(result.is_pii)
        self.assertEqual(result.pii_type, "email")
        self.assertEqual(result.sensitivity, "high")

    def test_customer_id_is_medium_risk_pii(self):
        result = classify_column("customer_id")

        self.assertTrue(result.is_pii)
        self.assertEqual(result.pii_type, "customer_identifier")
        self.assertEqual(result.sensitivity, "medium")

    def test_revenue_is_sensitive_but_not_pii(self):
        result = classify_column("total_revenue")

        self.assertFalse(result.is_pii)
        self.assertEqual(result.pii_type, "business_financial")
        self.assertEqual(result.sensitivity, "medium")

    def test_unknown_column_is_not_sensitive(self):
        result = classify_column("product_category")

        self.assertFalse(result.is_pii)
        self.assertIsNone(result.pii_type)
        self.assertEqual(result.sensitivity, "none")

    def test_summary_marks_high_risk_when_pii_exists(self):
        columns = classify_columns(
            [
                {"name": "customer_id"},
                {"name": "email"},
                {"name": "region"},
            ]
        )

        summary = summarize_pii(columns)

        self.assertTrue(summary["contains_pii"])
        self.assertEqual(summary["pii_column_count"], 2)
        self.assertEqual(summary["risk_level"], "high")


if __name__ == "__main__":
    unittest.main()
