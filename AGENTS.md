# AGENTS.md

Este repositorio corresponde a un Proyecto Final de Ingeniería sobre análisis asistido de resonancias magnéticas lumbares sagitales.

## Objetivo del proyecto

Desarrollar un prototipo académico que permita:

- cargar y preprocesar RM lumbares sagitales;
- segmentar vértebras, discos intervertebrales y canal espinal;
- calcular mediciones geométricas simples derivadas de máscaras;
- visualizar máscaras superpuestas;
- exportar resultados estructurados y editables para revisión profesional.

## Restricciones importantes

- El sistema no debe emitir diagnósticos.
- El sistema no debe recomendar tratamientos.
- El sistema no debe reemplazar el criterio profesional.
- Las mediciones deben presentarse como valores geométricos derivados de máscaras.
- La salida debe ser revisable y editable.
- No usar datos sensibles ni identificables de pacientes.
- No subir datasets, checkpoints ni resultados pesados al repositorio.
- Priorizar herramientas open source.
- Mantener el proyecto como prototipo académico reproducible.

## Convenciones técnicas

- Usar Python como lenguaje principal.
- Usar PyTorch para modelos de segmentación.
- Mantener funciones reutilizables dentro de `src/lumbar_mri/`.
- Mantener notebooks solamente como capa de experimentación y ejecución.
- Agregar tests para métricas, mediciones y exportación cuando sea posible.
- Documentar decisiones técnicas en `docs/decisiones_tecnicas.md`.
- Evitar sobreingeniería: primero pipeline completo, luego optimización.

## Flujo con Colab

Colab debe clonar o actualizar el repositorio desde GitHub. Los datos, checkpoints y outputs deben estar en Google Drive u otra ubicación externa, no dentro del repositorio.

## Validación

Cuando se modifique código funcional, intentar ejecutar:

```bash
pytest
```

Si se agregan funciones de inferencia, métricas o mediciones, agregar tests mínimos con arrays sintéticos.

## Estilo

- Código claro y simple.
- Funciones pequeñas y reutilizables.
- Nombres explícitos.
- Documentar supuestos.
- Separar código de experimentos.
