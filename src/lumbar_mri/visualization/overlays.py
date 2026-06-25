"""Funciones de visualización para overlays de segmentación."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def plot_image_and_mask(
    image: np.ndarray,
    mask: np.ndarray,
    alpha: float = 0.35,
    title: str | None = None,
):
    """Grafica imagen base y máscara superpuesta.

    La función devuelve `(fig, ax)` para permitir guardado o ajustes desde notebooks.
    """

    image = np.asarray(image)
    mask = np.asarray(mask)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(image, cmap="gray")
    masked = np.ma.masked_where(mask == 0, mask)
    ax.imshow(masked, alpha=alpha)
    ax.axis("off")
    if title:
        ax.set_title(title)
    return fig, ax


def plot_prediction_comparison(
    image: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
):
    """Grafica comparación simple entre ground truth y predicción."""

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Imagen")
    axes[1].imshow(image, cmap="gray")
    axes[1].imshow(np.ma.masked_where(y_true == 0, y_true), alpha=0.35)
    axes[1].set_title("Ground truth")
    axes[2].imshow(image, cmap="gray")
    axes[2].imshow(np.ma.masked_where(y_pred == 0, y_pred), alpha=0.35)
    axes[2].set_title("Predicción")
    for ax in axes:
        ax.axis("off")
    return fig, axes
