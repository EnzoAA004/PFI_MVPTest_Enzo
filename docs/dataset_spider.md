# Dataset SPIDER

## Uso previsto

SPIDER será utilizado como fuente principal para el MVP porque contiene resonancias magnéticas lumbares sagitales con máscaras de referencia para estructuras anatómicas alineadas con el alcance del proyecto.

## Estructuras de interés

- Vértebras.
- Discos intervertebrales.
- Canal espinal.

## Decisiones de manejo de datos

- El dataset no se sube a GitHub.
- El dataset debe almacenarse en Google Drive u otra ubicación externa.
- Colab debe montar Drive y configurar la ruta mediante variables de entorno o `src/lumbar_mri/config.py`.
- Las particiones de entrenamiento, validación y prueba deben realizarse por paciente cuando sea posible.

## Estructura sugerida en Drive

```text
/MyDrive/PFI_MVP/
├── data/
│   └── SPIDER/
├── models/
│   └── checkpoints/
└── outputs/
    ├── predictions/
    ├── measurements/
    ├── figures/
    └── reports/
```

## Pendientes

- Confirmar estructura exacta de archivos descargados.
- Implementar loader específico de SPIDER.
- Documentar clases originales y mapeo a clases del MVP.
- Documentar split por paciente.
