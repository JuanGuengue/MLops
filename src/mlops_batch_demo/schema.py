import json
from pathlib import Path

import pandas as pd

from .config import REQUIRED_COLUMNS, SCHEMA_REPORT_PATH


def validate_batch_dataframe(batch_df: pd.DataFrame) -> dict:
    """Valida estructura minima antes de dejar pasar el batch al scoring."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in batch_df.columns]
    duplicate_customer_ids = int(batch_df["customer_id"].duplicated().sum()) if "customer_id" in batch_df.columns else 0

    null_counts = {
        column: int(batch_df[column].isna().sum())
        for column in REQUIRED_COLUMNS
        if column in batch_df.columns
    }

    numeric_columns = ["monthly_charges", "support_tickets", "late_payments", "tenure_months"]
    negative_value_issues = {
        column: int((batch_df[column] < 0).sum())
        for column in numeric_columns
        if column in batch_df.columns
    }

    is_valid = (
        not missing_columns
        and duplicate_customer_ids == 0
        and all(count == 0 for count in null_counts.values())
        and all(count == 0 for count in negative_value_issues.values())
    )

    return {
        "is_valid": is_valid,
        "rows_received": int(len(batch_df)),
        "missing_columns": missing_columns,
        "duplicate_customer_ids": duplicate_customer_ids,
        "null_counts": null_counts,
        "negative_value_issues": negative_value_issues,
    }


def validate_batch_file(input_path: Path) -> dict:
    """Lee el CSV, ejecuta validaciones y deja un reporte legible para auditoria."""
    batch_df = pd.read_csv(input_path)
    report = validate_batch_dataframe(batch_df)

    SCHEMA_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if not report["is_valid"]:
        raise ValueError(f"Batch invalido: {json.dumps(report, ensure_ascii=False)}")

    return report

