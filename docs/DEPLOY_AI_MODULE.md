# Deploy del AI Module

El AI Module se despliega como un servicio Docker FastAPI consumido por el backend Spring Boot.

```text
Frontend React -> Spring Boot Backend -> Python FastAPI AI Module
```

El servicio es asistivo: no emite diagnostico clinico, no recomienda tratamientos y no toma decisiones medicas automaticas. Las respuestas de inferencia, pipeline y agente deben preservar `human_review_required=true` o `humanReviewRequired=true`.

## Dockerfile

El Dockerfile en `ai_service/Dockerfile`:

- usa `python:3.11-slim`;
- instala `ai_service/requirements-ai-service.txt`;
- copia `pfi_ai_service/`;
- expone puerto `8000`;
- ejecuta `uvicorn pfi_ai_service.api:app`;
- respeta `PORT` dinamico mediante `${PORT:-8000}`.

Comando ejecutado por la imagen:

```bash
uvicorn pfi_ai_service.api:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Variables necesarias

```text
PORT=8000
PFI_ROOT=/content/drive/MyDrive/PFI_MVP
PFI_MODEL_REGISTRY=config/model_registry_final.json
PFI_DATA_FREEZE_CONFIG=config/data_freeze_config.json
PFI_OUTPUT_DIR=outputs
```

Ver tambien `docs/CLOUD_ENVIRONMENT_VARIABLES.md`.

En produccion, `PFI_ROOT` debe apuntar a un volumen, bucket montado o ruta interna donde esten disponibles modelos y artefactos tecnicos autorizados. No incluir datasets completos, imagenes medicas privadas ni checkpoints pesados dentro de la imagen Docker salvo decision explicita del proyecto.

## Docker local

Desde la raiz del repositorio:

```bash
cd ai_service
docker build -t pfi-ai-module .
docker run --rm -p 8000:8000 --env-file ../.env.example pfi-ai-module
```

En otra terminal:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/models
```

Pipeline demo:

```bash
curl -X POST http://localhost:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"caseId":"case-demo-001","plane":"sagittal","modelKey":"sagittal_spider","inputPath":"demo/case-demo-001","metadata":{"source":"docker-smoke"}}'
```

## Render Docker Web Service

1. Crear un nuevo Web Service desde el repositorio.
2. Seleccionar entorno Docker.
3. Configurar root/contexto `ai_service` o indicar `ai_service/Dockerfile`, segun la configuracion de Render.
4. Definir variables de entorno:
   - `PORT`
   - `PFI_ROOT`
   - `PFI_MODEL_REGISTRY`
   - `PFI_DATA_FREEZE_CONFIG`
   - `PFI_OUTPUT_DIR`
5. Configurar almacenamiento externo para modelos/resultados, o un mecanismo de descarga controlado al arranque si el proyecto lo autoriza.
6. Usar `/health` como health check.

Render inyecta `PORT`; la imagen respeta ese valor.

## Railway Docker

1. Crear un nuevo servicio desde el repositorio.
2. Usar despliegue Docker con contexto `ai_service` o configurar la ruta del Dockerfile.
3. Cargar las variables de entorno necesarias.
4. Conectar almacenamiento externo para modelos, outputs y reportes.
5. Probar `/health`, `/models` y `/pipeline/run` con payload demo.

Railway define `PORT` durante ejecucion; la imagen lo toma mediante `${PORT:-8000}`.

## Google Cloud Run

1. Construir y subir la imagen a Artifact Registry.
2. Crear un servicio Cloud Run apuntando a la imagen.
3. Configurar variables de entorno.
4. Conectar acceso a Cloud Storage, Secret Manager o volumen compatible para modelos/resultados.
5. Preferir invocacion autenticada desde el backend Spring Boot.
6. Restringir acceso publico si el AI Module solo debe ser consumido internamente.

Ejemplo conceptual:

```bash
gcloud run deploy pfi-ai-module \
  --image REGION-docker.pkg.dev/PROJECT/REPOSITORY/pfi-ai-module:TAG \
  --region REGION \
  --set-env-vars PFI_ROOT=/mnt/pfi,PFI_OUTPUT_DIR=outputs \
  --no-allow-unauthenticated
```

## CI/CD

El workflow `.github/workflows/ai-module-ci.yml` es liviano:

- instala dependencias del AI service;
- ejecuta `python -m compileall ai_service/pfi_ai_service`;
- ejecuta `python scripts/smoke_api_contract.py`.

No requiere modelos pesados, datasets ni imagenes medicas reales.

## Advertencias sobre modelos y datasets

- No subir datasets completos al repositorio.
- No incluir imagenes medicas privadas en Git ni en imagenes Docker publicas.
- No borrar modelos, notebooks o resultados existentes sin confirmacion.
- Si los pesos son parte de la entrega y pesan demasiado, evaluar Git LFS o almacenamiento externo versionado.
- Registrar version de modelo, configuracion y limitaciones tecnicas junto con cada corrida.

## Estado para deploy

El modulo esta listo para deploy cloud como contrato tecnico/smoke. La inferencia real debe conectarse a modelos y almacenamiento externo autorizados antes de usar datos reales.
