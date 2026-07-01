# Variables de entorno cloud

| Variable | Ejemplo | Obligatoria | Descripcion |
| --- | --- | --- | --- |
| `PORT` | `8000` | Si | Puerto HTTP del servicio. Render, Railway y Cloud Run pueden inyectarlo dinamicamente. |
| `PFI_ROOT` | `/mnt/pfi` | Si | Raiz externa para modelos, resultados, figuras y reportes tecnicos. No debe apuntar a datos privados versionados en Git. |
| `PFI_MODEL_REGISTRY` | `config/model_registry_final.json` | Si | Ruta al registro tecnico de modelos. Puede ser ruta interna del contenedor o montada desde almacenamiento controlado. |
| `PFI_DATA_FREEZE_CONFIG` | `config/data_freeze_config.json` | Si | Ruta a la configuracion de congelamiento/criterios de datos para reproducibilidad academica. |
| `PFI_OUTPUT_DIR` | `outputs` | Si | Directorio de salida para reportes, overlays y artefactos tecnicos generados por el AI Module. |

## Notas

- No configurar rutas que expongan datasets completos o imagenes medicas reales en servicios publicos.
- No guardar secretos en `.env.example`.
- En Cloud Run o servicios equivalentes, usar Secret Manager o variables protegidas para credenciales de almacenamiento.
- El AI Module debe responder con `human_review_required=true` o `humanReviewRequired=true` en resultados de inferencia, pipeline y agente.
