import json
from pathlib import Path

import pandas as pd

from .config import FEATURE_COLUMNS, MONITORING_REPORT_PATH


def build_monitoring_report(reference_path: Path, current_batch_path: Path) -> dict:
    """
    Compara el batch actual contra una referencia.
    Para un demo junior, la señal de drift se explica con cambios fuertes de promedio.
    """
    reference_df = pd.read_csv(reference_path)
    current_df = pd.read_csv(current_batch_path)

    features_report = {}
    drift_detected = False

    for column in FEATURE_COLUMNS:
        reference_mean = float(reference_df[column].mean())
        current_mean = float(current_df[column].mean())
        mean_shift = current_mean - reference_mean

        # Umbral simple: si el batch se mueve más de 20%, marcamos alerta.
        denominator = abs(reference_mean) if reference_mean != 0 else 1.0
        relative_shift = abs(mean_shift) / denominator
        column_drift = relative_shift > 0.20

        features_report[column] = {
            "reference_mean": round(reference_mean, 4),
            "current_mean": round(current_mean, 4),
            "mean_shift": round(mean_shift, 4),
            "relative_shift": round(relative_shift, 4),
            "drift_detected": column_drift,
        }
        drift_detected = drift_detected or column_drift

    report = {
        "drift_detected": drift_detected,
        "features": features_report,
        "recommendation": (
            "Revisar el origen del batch antes de promover resultados."
            if drift_detected
            else "El batch se mantiene dentro del comportamiento esperado."
        ),
    }

    MONITORING_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

