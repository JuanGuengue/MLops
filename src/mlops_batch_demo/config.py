from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
REFERENCE_DIR = DATA_DIR / "reference"
OUTPUT_DIR = DATA_DIR / "output"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"

MODEL_PATH = ARTIFACTS_DIR / "approved_customer_risk_model.joblib"
SCHEMA_REPORT_PATH = OUTPUT_DIR / "validation_report.json"
SCORED_BATCH_PATH = OUTPUT_DIR / "scored_customers.csv"
MONITORING_REPORT_PATH = OUTPUT_DIR / "monitoring_report.json"
BASELINE_DATA_PATH = REFERENCE_DIR / "baseline_customers.csv"
BATCH_DATA_PATH = INPUT_DIR / "customers_batch.csv"

REQUIRED_COLUMNS = [
    "customer_id",
    "monthly_charges",
    "support_tickets",
    "late_payments",
    "tenure_months",
]

FEATURE_COLUMNS = [
    "monthly_charges",
    "support_tickets",
    "late_payments",
    "tenure_months",
]

