from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PiiClassification:
    is_pii: bool
    pii_type: str | None
    sensitivity: str
    reason: str


PII_COLUMN_RULES = {
    "email": ("email", "high"),
    "email_address": ("email", "high"),
    "phone": ("phone_number", "high"),
    "phone_number": ("phone_number", "high"),
    "full_name": ("person_name", "high"),
    "first_name": ("person_name", "high"),
    "last_name": ("person_name", "high"),
    "customer_id": ("customer_identifier", "medium"),
    "user_id": ("user_identifier", "medium"),
    "account_id": ("account_identifier", "medium"),
    "address": ("postal_address", "high"),
    "date_of_birth": ("date_of_birth", "high"),
    "dob": ("date_of_birth", "high"),
    "passport_number": ("government_identifier", "restricted"),
    "aadhaar_number": ("government_identifier", "restricted"),
    "pan_number": ("government_identifier", "restricted"),
}

SENSITIVE_BUSINESS_COLUMNS = {
    "net_amount": "business_financial",
    "total_revenue": "business_financial",
    "list_price": "business_financial",
    "trust_score": "governance_score",
}


def normalize_column_name(column_name: str) -> str:
    return column_name.strip().lower()


def classify_column(column_name: str) -> PiiClassification:
    normalized_name = normalize_column_name(column_name)

    if normalized_name in PII_COLUMN_RULES:
        pii_type, sensitivity = PII_COLUMN_RULES[normalized_name]
        return PiiClassification(
            is_pii=True,
            pii_type=pii_type,
            sensitivity=sensitivity,
            reason=f"Column name '{column_name}' matched the {pii_type} PII rule.",
        )

    if normalized_name.endswith("_email"):
        return PiiClassification(
            is_pii=True,
            pii_type="email",
            sensitivity="high",
            reason=f"Column name '{column_name}' ends with _email.",
        )

    if normalized_name.endswith("_phone"):
        return PiiClassification(
            is_pii=True,
            pii_type="phone_number",
            sensitivity="high",
            reason=f"Column name '{column_name}' ends with _phone.",
        )

    if normalized_name in SENSITIVE_BUSINESS_COLUMNS:
        return PiiClassification(
            is_pii=False,
            pii_type=SENSITIVE_BUSINESS_COLUMNS[normalized_name],
            sensitivity="medium",
            reason=f"Column name '{column_name}' is business sensitive but not personal data.",
        )

    return PiiClassification(
        is_pii=False,
        pii_type=None,
        sensitivity="none",
        reason=f"Column name '{column_name}' did not match a sensitive data rule.",
    )


def classify_columns(columns: list[dict]) -> list[dict]:
    classified_columns = []
    for column in columns:
        classification = classify_column(column["name"])
        enriched_column = dict(column)
        enriched_column.update(
            {
                "is_pii": classification.is_pii,
                "pii_type": classification.pii_type,
                "sensitivity": classification.sensitivity,
                "classification_reason": classification.reason,
            }
        )
        classified_columns.append(enriched_column)
    return classified_columns


def summarize_pii(columns: list[dict]) -> dict:
    pii_columns = [column for column in columns if column["is_pii"]]
    sensitive_columns = [
        column
        for column in columns
        if column["sensitivity"] != "none" and not column["is_pii"]
    ]
    sensitivities = {column["sensitivity"] for column in columns}

    if "restricted" in sensitivities:
        risk_level = "restricted"
    elif pii_columns:
        risk_level = "high"
    elif sensitive_columns:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "contains_pii": bool(pii_columns),
        "pii_column_count": len(pii_columns),
        "sensitive_column_count": len(sensitive_columns),
        "risk_level": risk_level,
        "pii_columns": [
            {
                "name": column["name"],
                "pii_type": column["pii_type"],
                "sensitivity": column["sensitivity"],
            }
            for column in pii_columns
        ],
        "sensitive_columns": [
            {
                "name": column["name"],
                "sensitivity_type": column["pii_type"],
                "sensitivity": column["sensitivity"],
            }
            for column in sensitive_columns
        ],
    }
