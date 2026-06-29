import unittest

from governance_platform.vector_store import point_id, record_to_point


class VectorStoreTest(unittest.TestCase):
    def test_point_id_is_deterministic_integer(self):
        self.assertEqual(point_id("raw.customers::asset"), point_id("raw.customers::asset"))
        self.assertIsInstance(point_id("raw.customers::asset"), int)

    def test_record_to_point_preserves_payload(self):
        point = record_to_point(
            {
                "chunk_id": "raw.customers::asset",
                "asset_id": "raw.customers",
                "chunk_type": "asset_summary",
                "text": "Asset: raw.customers",
                "metadata": {"contains_pii": True},
                "embedding_model": "local_hashing_embedding_v1",
                "embedding": [0.1, 0.2],
            }
        )

        self.assertEqual(point["payload"]["asset_id"], "raw.customers")
        self.assertEqual(point["payload"]["metadata"]["contains_pii"], True)
        self.assertEqual(point["vector"], [0.1, 0.2])


if __name__ == "__main__":
    unittest.main()
