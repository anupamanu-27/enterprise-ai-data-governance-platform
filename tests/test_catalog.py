import unittest

from governance_platform.catalog import (
    calculate_effective_trust_score,
    default_asset_metadata,
    display_name,
    quality_by_asset,
    trust_band,
)


class CatalogTest(unittest.TestCase):
    def test_display_name_formats_table_names(self):
        self.assertEqual(display_name("mart_customer_revenue"), "Mart Customer Revenue")

    def test_default_asset_metadata_uses_analytics_owner(self):
        asset = default_asset_metadata("analytics_marts", "mart_customer_revenue")

        self.assertEqual(asset.business_domain, "Analytics")
        self.assertEqual(asset.owner_name, "Data Platform Team")
        self.assertEqual(asset.base_trust_score, 90)

    def test_quality_report_is_indexed_by_qualified_name(self):
        lookup = quality_by_asset(
            {
                "assets": [
                    {
                        "qualified_name": "analytics_marts.mart_customer_revenue",
                        "success": True,
                        "row_count": 4,
                        "passed_checks": 7,
                        "failed_checks": 0,
                        "total_checks": 7,
                    }
                ]
            }
        )

        self.assertTrue(lookup["analytics_marts.mart_customer_revenue"]["success"])

    def test_effective_trust_score_rewards_passing_quality(self):
        score = calculate_effective_trust_score(
            90,
            {"success": True, "failed_checks": 0},
        )

        self.assertEqual(score, 95)

    def test_effective_trust_score_penalizes_failed_checks(self):
        score = calculate_effective_trust_score(
            90,
            {"success": False, "failed_checks": 3},
        )

        self.assertEqual(score, 60)

    def test_trust_band(self):
        self.assertEqual(trust_band(90), "high_trust")
        self.assertEqual(trust_band(75), "medium_trust")
        self.assertEqual(trust_band(60), "needs_attention")


if __name__ == "__main__":
    unittest.main()
