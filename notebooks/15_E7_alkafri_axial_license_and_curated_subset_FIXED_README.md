# Notebook 15 fixed runner

Se agregó una versión robusta del flujo del notebook 15 en:

`notebooks/15_E7_alkafri_axial_license_and_curated_subset_fixed.py`

## Para usarlo en Colab

Después de hacer `git pull` en el repositorio clonado en Drive, correr una celda con:

```python
%run /content/drive/MyDrive/PFI_MVP/repo/notebooks/15_E7_alkafri_axial_license_and_curated_subset_fixed.py
```

## Qué corrige

- No depende de que existan `E6_alkafri_axial_ima_candidates.csv`, `E6_alkafri_axial_series_summary.csv` o `E6_alkafri_ground_truth_real_files.csv`.
- Si esos CSV faltan, reconstruye los índices desde:
  - `E6_alkafri_image_specific_tokens.csv`
  - `E6_alkafri_gt_specific_tokens.csv`
  - `E6_alkafri_final_gt_png_tokens.csv`
- Normaliza `case_id` a cuatro dígitos para evitar errores tipo `37` vs `0037`.
- Calcula solapamiento `case_id + modality`.
- Genera candidatos estrictos sin asumir que `D3/D4/D5` equivale a `InstanceNumber` DICOM.
- Genera figuras de curación, sanity checks y hoja editable de revisión.
- Solo crea `axial_curated_v1` si hay al menos 30 pares aceptados.

## Salidas principales

En Drive:

`/content/drive/MyDrive/PFI_MVP/results/E7_alkafri_axial_curated_subset/`

Archivos esperados:

- `E7_alkafri_dataset_license_audit.csv`
- `E7_alkafri_axial_image_case_index.csv`
- `E7_alkafri_gt_case_index.csv`
- `E7_alkafri_case_modality_overlap_diagnosis.csv`
- `E7_alkafri_axial_strict_candidate_pairs.csv`
- `E7_alkafri_axial_curation_review_sheet.csv`
- `E7_alkafri_axial_candidate_sanity_checks.csv`
- `E7_alkafri_axial_auto_curated_candidates.csv`
- `E7_alkafri_axial_curated_feasibility_assessment.json`
- `E7_alkafri_axial_license_and_curated_subset_report.json`

## Revisión manual

Si se quiere forzar una curación manual, editar:

`E7_alkafri_axial_curation_review_sheet.csv`

Guardar una copia como:

`E7_alkafri_axial_curation_review_sheet_MANUAL.csv`

Y marcar `manual_accept = yes` en las filas aceptadas.

Luego volver a ejecutar el script.
