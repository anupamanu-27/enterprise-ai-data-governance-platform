from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from quality.gx_quality_checks import run_quality_checks


def main() -> int:
    report = run_quality_checks()
    print(
        "Quality checks completed: "
        f"{report['total_checks'] - report['failed_checks']}/{report['total_checks']} checks passed"
    )
    print("Report written to quality/reports/latest_quality_report.json")
    return 0 if report["overall_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
