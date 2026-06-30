# Cierre PF-001 a PF-003 - Base final de datos, splits e inventario

Estado: cerrado.

## Objetivo

Estandarizar la base de datos final del producto, congelar splits reproducibles y documentar inventario/licencias antes de avanzar con entrenamiento definitivo y endpoints reales.

## Resultado principal

La base de datos queda lista para la etapa de entrenamiento final.

Decision reportada:

```text
PF001_PF003_dataset_base_ready_for_final_training
```

## Checks

Todos los checks fueron correctos:

- spider_root_exists: true
- axial_root_exists: true
- canonical_config_written: true
- physical_inventory_written: true
- split_manifest_written: true
- dataset_inventory_written: true
- license_doc_written: true
- has_split_rows: true, rows=2013
- has_dataset_inventory_rows: true, rows=3

## Inventario fisico resumido

### SPIDER sagital

- raiz: `/content/drive/MyDrive/PFI_MVP/data/SPIDER`
- existe: true
- archivos `.mha`: 894
- zips: 2
- csv: 2
- rol: dataset principal sagital del MVP

### Al-Kafri / Sudirman axial

- raiz: `/content/drive/MyDrive/PFI_MVP/data/AXIAL_ALKAFRI`
- existe: true
- archivos `.ima`: 17497
- imagenes/labels `.png`: 29361
- archivos `.mat`: 32
- archivos `.npy`: 1436
- zips: 7
- rol: dataset complementario axial del MVP

### SSMSpine opcional

- raiz: `/content/drive/MyDrive/PFI_MVP/data/SSMSPINE`
- existe: true
- archivos `.pt`: 250
- zips: 2
- rol: fuera del nucleo actual; no usar en metricas finales sin licencia y decision explicita

## Splits congelados

Se genero un manifest con 2013 filas para los datasets del alcance final.

### SPIDER sagital

- train: 279 imagenes + 279 mascaras, 150 casos unicos
- val: 69 imagenes + 69 mascaras, 36 casos unicos
- test: 58 imagenes + 58 mascaras, 30 casos unicos

### Al-Kafri / Sudirman axial

- train: 856 pares candidatos oficiales, 132 casos unicos
- val: 186 pares candidatos oficiales, 28 casos unicos
- test: 159 pares candidatos oficiales, 24 casos unicos

## Archivos generados

- `config/data_freeze_config.json`
- `docs/PF001_PF003_dataset_licenses.md`
- `results/PF001_PF003_dataset_freeze/PF001_canonical_data_paths.json`
- `results/PF001_PF003_dataset_freeze/PF001_physical_file_inventory.csv`
- `results/PF001_PF003_dataset_freeze/PF001_physical_file_inventory_summary.csv`
- `results/PF001_PF003_dataset_freeze/PF002_discovered_split_sources.csv`
- `results/PF001_PF003_dataset_freeze/PF002_final_splits_manifest.csv`
- `results/PF001_PF003_dataset_freeze/PF002_split_summary.csv`
- `results/PF001_PF003_dataset_freeze/PF003_dataset_inventory.csv`
- `results/PF001_PF003_dataset_freeze/PF003_dataset_licenses.md`
- `results/PF001_PF003_dataset_freeze/PF001_PF003_checks.csv`
- `results/PF001_PF003_dataset_freeze/PF001_PF003_report.json`

## Politica metodologica

- human_review_required: true
- not_clinical_diagnosis: true
- not_real_3d_reconstruction: true
- final_product_scope: MVP tecnico demostrable con inferencia 2D multiplanar, agente y revision profesional

## Proximo bloque

PF-004 a PF-007:

- entrenamiento/modelos finales,
- consolidacion de checkpoints,
- configuracion unica de modelos,
- reporte definitivo de metricas.
