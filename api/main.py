from pathlib import Path
import sys

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mlops_batch_demo.config import MODEL_PATH


app = FastAPI(title="Batch Scoring Demo API", version="1.0.0")


class CustomerRequest(BaseModel):
    monthly_charges: float = Field(..., ge=0)
    support_tickets: int = Field(..., ge=0)
    late_payments: int = Field(..., ge=0)
    tenure_months: int = Field(..., ge=0)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Modelo no disponible. Ejecuta scripts/bootstrap_approved_model.py"
        )
    return joblib.load(MODEL_PATH)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "batch-scoring-demo"}


@app.post("/predict")
def predict(payload: CustomerRequest) -> dict:
    try:
        model = load_model()
        features = np.array(
            [
                payload.monthly_charges,
                payload.support_tickets,
                payload.late_payments,
                payload.tenure_months,
            ],
            dtype=float,
        ).reshape(1, -1)

        probability = float(model.predict_proba(features)[0][1])
        prediction = int(probability >= 0.50)
        return {
            "risk_prediction": prediction,
            "risk_probability": round(probability, 4),
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

