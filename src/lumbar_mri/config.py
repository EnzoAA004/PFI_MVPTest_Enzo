"""Configuración central del proyecto.

Las rutas por defecto apuntan a una estructura típica montada en Google Drive.
Pueden sobrescribirse con variables de entorno.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Rutas principales del proyecto."""

    data_root: Path
    model_dir: Path
    output_dir: Path


def get_project_paths() -> ProjectPaths:
    """Devuelve rutas configurables para datos, modelos y salidas."""

    default_base = Path("/content/drive/MyDrive/PFI_MVP")
    base = Path(os.getenv("PFI_MVP_ROOT", default_base))

    return ProjectPaths(
        data_root=Path(os.getenv("PFI_DATA_ROOT", base / "data" / "SPIDER")),
        model_dir=Path(os.getenv("PFI_MODEL_DIR", base / "models" / "checkpoints")),
        output_dir=Path(os.getenv("PFI_OUTPUT_DIR", base / "outputs")),
    )


CLASSES = {
    0: "background",
    1: "vertebra",
    2: "disc",
    3: "spinal_canal",
}
