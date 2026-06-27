import tempfile
from pathlib import Path
import unittest

from governance_platform.ingestion import (
    build_campaign_insert_sql,
    read_campaign_rows,
)


class CampaignIngestionTest(unittest.TestCase):
    def test_reads_campaign_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = Path(temp_dir) / "campaigns.csv"
            source_file.write_text(
                "campaign_id,campaign_name,channel,region,budget,start_date,end_date,owner_name\n"
                "CMP-TEST,Test Campaign,Email,West,100.00,2025-01-01,2025-01-31,Test Owner\n",
                encoding="utf-8",
            )

            rows = read_campaign_rows(source_file)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["campaign_id"], "CMP-TEST")

    def test_missing_required_column_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = Path(temp_dir) / "campaigns.csv"
            source_file.write_text(
                "campaign_id,campaign_name\nCMP-TEST,Test Campaign\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                read_campaign_rows(source_file)

    def test_build_campaign_insert_sql_is_idempotent(self) -> None:
        rows = [
            {
                "campaign_id": "CMP-TEST",
                "campaign_name": "Test Campaign",
                "channel": "Email",
                "region": "West",
                "budget": "100.00",
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
                "owner_name": "Test Owner",
            }
        ]

        sql = build_campaign_insert_sql(rows)

        self.assertIn("CREATE TABLE IF NOT EXISTS raw.marketing_campaigns", sql)
        self.assertIn("ON CONFLICT (campaign_id) DO UPDATE", sql)


if __name__ == "__main__":
    unittest.main()

