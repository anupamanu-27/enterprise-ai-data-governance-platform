import unittest

from quality.gx_quality_checks import QUALITY_ASSETS, expectations_for, to_json_safe


class QualityChecksTest(unittest.TestCase):
    def test_quality_assets_are_configured(self):
        asset_names = {asset.name for asset in QUALITY_ASSETS}

        self.assertIn("customer_revenue_mart", asset_names)
        self.assertIn("governance_asset_health_mart", asset_names)

    def test_each_asset_has_expectations(self):
        for asset in QUALITY_ASSETS:
            with self.subTest(asset=asset.name):
                self.assertGreaterEqual(len(expectations_for(asset)), 5)

    def test_nan_values_are_json_safe(self):
        result = to_json_safe({"values": [1.0, float("nan")]})

        self.assertEqual(result, {"values": [1.0, None]})


if __name__ == "__main__":
    unittest.main()
