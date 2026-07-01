# Evidencia final del AI Module

## Commit actual

Validacion preparada sobre:

```text
bbf2f99 Validate AI module for local E2E integration
```

Este documento forma parte del commit de preparacion para deploy cloud y evidencia final.

## Endpoints disponibles

- `GET /health`
- `GET /models`
- `POST /inference/sagittal`
- `POST /inference/axial`
- `POST /pipeline/run`
- `GET /agent/worklist`
- `GET /agent/report`
- `GET /agent/report/{run_id}`
- `GET /agent/regression-test`

## Comando local

Desde la raiz del repositorio:

```bash
cd ai_service
uvicorn pfi_ai_service.api:app --host 0.0.0.0 --port ${PORT:-8000}
```

En Windows, usando el venv local desde la raiz del repo:

```powershell
.\.venv\Scripts\python.exe -m uvicorn pfi_ai_service.api:app --host 0.0.0.0 --port 8000
```

## Comando Docker

```bash
cd ai_service
docker build -t pfi-ai-module .
docker run --rm -p 8000:8000 --env-file ../.env.example pfi-ai-module
```

## Ejemplo curl /health

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "pfi_root": "/content/drive/MyDrive/PFI_MVP",
  "human_review_required": true
}
```

## Ejemplo curl /models

```bash
curl http://localhost:8000/models
```

Respuesta resumida esperada:

```json
{
  "models": {
    "sagittal_spider": {
      "plane": "sagittal",
      "human_review_required": true
    },
    "axial_t2_alkafri": {
      "plane": "axial",
      "human_review_required": true
    }
  },
  "paths": {
    "sagittal_model_path": "models/final/sagittal_spider_multiclass_final_best.pt",
    "axial_model_path": "models/final/axial_t2_alkafri_final_best.pt"
  }
}
```

## Ejemplo curl /pipeline/run

```bash
curl -X POST http://localhost:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"caseId":"case-demo-001","plane":"sagittal","modelKey":"sagittal_spider","inputPath":"demo/case-demo-001","metadata":{"source":"final-evidence"}}'
```

Respuesta resumida esperada:

```json
{
  "runId": "a63014c107adef94",
  "caseId": "case-demo-001",
  "plane": "sagittal",
  "modelKey": "sagittal_spider",
  "measurements": {
    "status": "pending_real_inference",
    "values": []
  },
  "agentDecision": {
    "agent_status": "requires_professional_review",
    "human_review_required": true,
    "not_clinical_diagnosis": true
  },
  "humanReviewRequired": true,
  "notClinicalDiagnosis": true
}
```

## Validaciones ejecutadas

```bash
python -m compileall ai_service/pfi_ai_service
python scripts/smoke_api_contract.py
```

Resultado:

```text
compileall: OK
smoke_api_contract.py: AI Module contract smoke test passed.
```

## Limitaciones

- El pipeline actual valida contrato y trazabilidad tecnica, pero no ejecuta inferencia real sobre imagenes medicas.
- Los modelos, checkpoints, outputs pesados y datasets deben permanecer fuera del repositorio.
- Las rutas de modelos apuntan por defecto a `models/final` y pueden cambiarse mediante `PFI_MODEL_DIR`.
- La evidencia no contiene datos medicos reales ni privados.

## Aclaracion metodologica

El AI Module es asistivo. No emite diagnostico clinico, no recomienda tratamientos y no toma decisiones medicas automaticas. Toda salida de inferencia, pipeline o agente requiere revision profesional y debe preservar `human_review_required=true` o `humanReviewRequired=true`.
