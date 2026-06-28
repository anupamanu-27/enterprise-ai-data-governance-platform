from __future__ import annotations

from governance_platform.catalog import write_catalog


def main() -> int:
    catalog = write_catalog()
    print(f"Metadata catalog built with {catalog['asset_count']} assets")
    print("Catalog written to data/catalog/metadata_catalog.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
