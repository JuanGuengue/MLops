import json
import os
from pathlib import Path

import joblib
import mlflow
import pandas as pd

from .config import FEATURE_COLUMNS, MODEL_PATH, MLRUNS_DIR, OUTPUT_DIR, SCORED_BATCH_PATH


def _risk_label(probability: float) -> str:
    """Convierte una probabilidad tecnica en una etiqueta fácil de explicar."""
    if probability >= 0.75:
        return "alto"
    if probability >= 0.45:
        return "medio"
    return "bajo"


def score_batch_file(input_path: Path) -> dict:
    """Carga el modelo aprobado y genera un archivo de scoring batch."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "No existe el modelo aprobado. Ejecuta scripts/bootstrap_approved_model.py"
        )

    batch_df = pd.read_csv(input_path)
    model = joblib.load(MODEL_PATH)

    # Solo estas columnas entran al modelo; el resto se conserva para trazabilidad.
    features = batch_df[FEATURE_COLUMNS]
    probabilities = model.predict_proba(features)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    scored_df = batch_df.copy()
    scored_df["risk_probability"] = probabilities.round(4)
    scored_df["risk_prediction"] = predictions
    scored_df["risk_label"] = scored_df["risk_probability"].apply(_risk_label)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scored_df.to_csv(SCORED_BATCH_PATH, index=False)

    summary = {
        "rows_scored": int(len(scored_df)),
        "high_risk_customers": int((scored_df["risk_label"] == "alto").sum()),
        "average_risk_probability": float(scored_df["risk_probability"].mean()),
        "output_file": str(SCORED_BATCH_PATH),
    }

    # MLflow aqui registra la corrida operativa del scoring, no un experimento de entrenamiento.
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", f"file:{MLRUNS_DIR}"))
    mlflow.set_experiment("customer-batch-scoring")
    with mlflow.start_run(run_name="daily_batch_scoring"):
        mlflow.log_param("input_file", str(input_path))
        mlflow.log_metric("rows_scored", summary["rows_scored"])
        mlflow.log_metric("high_risk_customers", summary["high_risk_customers"])
        mlflow.log_metric("average_risk_probability", summary["average_risk_probability"])
        # mlflow.log_artifact(str(SCORED_BATCH_PATH)) error al intentar subir el CSV, asi que lo guardamos manualmente y luego subimos el JSON con el resumen.

        summary_path = OUTPUT_DIR / "scoring_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        #mlflow.log_artifact(str(summary_path)) error al intentar subir el JSON, asi que lo dejamos en el output local.

    return summary

