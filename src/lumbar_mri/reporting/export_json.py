"""Exportación JSON de resultados del MVP."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_result_document(
    study_id: str,
    model_version: str,
    measurements: list[dict[str, Any]],
    sequence: str | None = None,
) -> dict[str, Any]:
    """Construye una salida estructurada editable y no diagnóstica."""

    return {
        "study_id": study_id,
        "sequence": sequence,
        "model_version": model_version,
        "results": measurements,
        "reviewed_by_professional": False,
        "general_observations": "",
        "disclaimer": (
            "Salida geométrica derivada de máscaras. "
            "No constituye diagnóstico ni recomendación terapéutica."
        ),
    }


def save_json(document: dict[str, Any], path: str | Path) -> Path:
    """Guarda un documento JSON con indentación."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
