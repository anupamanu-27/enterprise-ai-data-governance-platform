import unittest

from governance_platform.embeddings import (
    EMBEDDING_DIMENSION,
    build_catalog_chunks,
    embed_text,
    tokenize,
)


class EmbeddingsTest(unittest.TestCase):
    def test_tokenize_normalizes_text(self):
        self.assertEqual(tokenize("Customer Revenue_Mart!"), ["customer", "revenue_mart"])

    def test_embed_text_has_expected_dimension(self):
        vector = embed_text("customer pii email")

        self.assertEqual(len(vector), EMBEDDING_DIMENSION)
        self.assertGreater(sum(vector), 0)

    def test_embed_text_is_deterministic(self):
        self.assertEqual(embed_text("same text"), embed_text("same text"))

    def test_build_catalog_chunks_creates_asset_and_column_chunks(self):
        catalog = {
            "assets": [
                {
                    "qualified_name": "raw.customers",
                    "asset_name": "Customers",
                    "description": "Raw customer master data.",
                    "owner_name": "Data Steward",
                    "business_domain": "Customer 360",
                    "trust_band": "medium_trust",
                    "effective_trust_score": 82,
                    "contains_pii": True,
                    "pii_summary": {
                        "risk_level": "high",
                        "pii_columns": [{"name": "email"}],
                    },
                    "lineage": {
                        "upstream_assets": [],
                        "downstream_assets": ["analytics_staging.stg_customers"],
                    },
                    "glossary_terms": [{"term_name": "PII"}],
                    "columns": [
                        {
                            "name": "email",
                            "data_type": "character varying",
                            "nullable": False,
                            "is_pii": True,
                            "pii_type": "email",
                            "sensitivity": "high",
                            "classification_reason": "Matched email rule.",
                        }
                    ],
                }
            ]
        }

        chunks = build_catalog_chunks(catalog)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].chunk_type, "asset_summary")
        self.assertEqual(chunks[1].chunk_type, "column_profile")


if __name__ == "__main__":
    unittest.main()
