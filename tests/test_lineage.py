import unittest

from governance_platform.lineage import (
    direct_downstreams,
    direct_upstreams,
    lineage_graph,
    lineage_summary,
    transitive_upstreams,
)


class LineageTest(unittest.TestCase):
    def test_customer_revenue_mart_has_expected_upstreams(self):
        upstreams = direct_upstreams("analytics_marts.mart_customer_revenue")

        self.assertIn("analytics_staging.stg_customers", upstreams)
        self.assertIn("analytics_staging.stg_sales_orders", upstreams)
        self.assertIn("raw.customers", upstreams)
        self.assertIn("raw.sales_orders", upstreams)

    def test_raw_customers_has_downstream_mart(self):
        downstreams = direct_downstreams("raw.customers")

        self.assertIn("analytics_marts.mart_customer_revenue", downstreams)

    def test_transitive_upstreams_include_raw_sources(self):
        upstreams = transitive_upstreams("analytics_marts.mart_customer_revenue")

        self.assertIn("raw.customers", upstreams)
        self.assertIn("raw.sales_orders", upstreams)

    def test_lineage_summary_contains_edges(self):
        summary = lineage_summary("analytics_marts.mart_governance_asset_health")

        self.assertEqual(summary["upstream_assets"], ["governance.data_assets"])
        self.assertEqual(len(summary["upstream_edges"]), 1)

    def test_lineage_graph_counts_nodes_and_edges(self):
        graph = lineage_graph()

        self.assertGreaterEqual(graph["node_count"], 8)
        self.assertGreaterEqual(graph["edge_count"], 8)


if __name__ == "__main__":
    unittest.main()
