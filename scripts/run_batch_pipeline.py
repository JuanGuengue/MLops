from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mlops_batch_demo.config import (
    BASELINE_DATA_PATH,
    BATCH_DATA_PATH,
    SCORED_BATCH_PATH,
)
from mlops_batch_demo.monitoring import build_monitoring_report
from mlops_batch_demo.schema import validate_batch_file
from mlops_batch_demo.scoring import score_batch_file


def main() -> None:
    # Paso 1: no dejamos correr el scoring si el archivo viene roto.
    validation_report = validate_batch_file(BATCH_DATA_PATH)
    print(f"Validacion OK: {validation_report}")

    # Paso 2: ejecutamos el modelo aprobado sobre el CSV recibido.
    scoring_summary = score_batch_file(BATCH_DATA_PATH)
    print(f"Scoring OK: {scoring_summary}")

    # Paso 3: comparamos el batch contra un baseline para monitoreo.
    monitoring_report = build_monitoring_report(BASELINE_DATA_PATH, SCORED_BATCH_PATH)
    print(f"Monitoreo OK: {monitoring_report}")


if __name__ == "__main__":
    main()
