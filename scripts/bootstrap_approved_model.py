from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mlops_batch_demo.config import ARTIFACTS_DIR, BASELINE_DATA_PATH, MODEL_PATH


def build_demo_model() -> None:
    """
    Este script solo fabrica un modelo demo ya aprobado.
    No es el foco del ejercicio; el foco real es operar el modelo.
    """
    training_df = pd.read_csv(BASELINE_DATA_PATH)

    # Etiqueta simple para generar un comportamiento de riesgo comprensible.
    target = (
        (training_df["monthly_charges"] > 95).astype(int)
        | (training_df["late_payments"] >= 2).astype(int)
        | (training_df["support_tickets"] >= 5).astype(int)
    ).astype(int)

    features = training_df[[
        "monthly_charges",
        "support_tickets",
        "late_payments",
        "tenure_months",
    ]]

    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(features, target)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modelo demo creado en: {MODEL_PATH}")


if __name__ == "__main__":
    build_demo_model()
