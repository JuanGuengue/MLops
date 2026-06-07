# MLOps Batch Scoring Demo

Proyecto MLOps pensado para explicar a analistas junior cómo operar un modelo ya aprobado sin entrar en detalle matemático de entrenamiento.

## Caso de negocio

Cada día llega un archivo CSV con clientes. El pipeline:

1. valida que el archivo esté bien formado,
2. ejecuta scoring sobre un modelo aprobado,
3. guarda resultados,
4. registra la corrida en MLflow,
5. compara el batch contra un baseline para monitoreo.

## Herramientas

- `Python`: lógica del pipeline
- `MLflow`: registro de corridas de scoring
- `Airflow`: orquestación diaria
- `FastAPI`: endpoint de predicción individual
- `Docker`: empaquetado
- `GitHub Actions`: CI/CD
- `AWS EC2`: despliegue objetivo

## Flujo funcional

- [schema.py](C:\Users\gueng\Downloads\mlops-batch-scoring-demo\src\mlops_batch_demo\schema.py): valida columnas, nulos y valores negativos
- [scoring.py](C:\Users\gueng\Downloads\mlops-batch-scoring-demo\src\mlops_batch_demo\scoring.py): carga el modelo aprobado y genera el CSV con riesgos
- [monitoring.py](C:\Users\gueng\Downloads\mlops-batch-scoring-demo\src\mlops_batch_demo\monitoring.py): compara el batch actual con una referencia histórica
- [batch_scoring_pipeline.py](C:\Users\gueng\Downloads\mlops-batch-scoring-demo\dags\batch_scoring_pipeline.py): DAG de Airflow

## Ejecutar local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/bootstrap_approved_model.py
python scripts/run_batch_pipeline.py
uvicorn api.main:app --reload --port 8001
```

## Ejecutar con Docker

```bash
docker compose up -d --build
```

Servicios:

- API: `http://localhost:8001/docs`
- MLflow: `http://localhost:5001`
- Airflow: `http://localhost:8081`

## Qué explicar en la exposición

- El modelo no se entrena en vivo; ya fue aprobado previamente.
- MLOps aquí se encarga de operar ese modelo con seguridad.
- La validación evita procesar archivos malos.
- MLflow deja trazabilidad de cada ejecución.
- Airflow automatiza la corrida diaria.
- El monitoreo alerta si el batch viene demasiado distinto al baseline.
