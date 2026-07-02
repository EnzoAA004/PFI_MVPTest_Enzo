from __future__ import annotations

from math import hypot
from typing import Any, Dict, Iterable, List, Optional, Tuple

Point = Dict[str, float]
Mask = Dict[str, Any]
Landmark = Dict[str, Any]
Measurement = Dict[str, Any]

PIXEL_SPACING_MM = 0.115


def contour_points(mask: Mask, series_id: str, slice_index: int) -> List[Point]:
    for contour in mask.get("contours", []):
        if contour.get("seriesId") == series_id and contour.get("sliceIndex") == slice_index:
            return list(contour.get("points", []))
    return []


def centroid(points: Iterable[Point]) -> Tuple[float, float]:
    values = list(points)
    if not values:
        return 0.0, 0.0
    return sum(float(point.get("x", 0.0)) for point in values) / len(values), sum(float(point.get("y", 0.0)) for point in values) / len(values)


def bounds(points: Iterable[Point]) -> Tuple[float, float, float, float]:
    values = list(points)
    if not values:
        return 0.0, 0.0, 0.0, 0.0
    xs = [float(point.get("x", 0.0)) for point in values]
    ys = [float(point.get("y", 0.0)) for point in values]
    return min(xs), min(ys), max(xs), max(ys)


def distance_mm(a: Point, b: Point) -> float:
    return round(hypot(float(a.get("x", 0.0)) - float(b.get("x", 0.0)), float(a.get("y", 0.0)) - float(b.get("y", 0.0))) * PIXEL_SPACING_MM, 1)


def mask_by_id(masks: List[Mask], mask_id: str) -> Optional[Mask]:
    return next((mask for mask in masks if mask.get("id") == mask_id), None)


def landmark_from_mask(mask: Mask, *, landmark_id: str, label: str, series_id: str, slice_index: int) -> Landmark:
    points = contour_points(mask, series_id, slice_index)
    x, y = centroid(points)
    return {
        "id": landmark_id,
        "label": label,
        "seriesId": series_id,
        "sliceIndex": slice_index,
        "x": round(x, 1),
        "y": round(y, 1),
        "editable": True,
        "linkedMaskId": mask.get("id"),
    }


def build_landmarks_from_masks(masks: List[Mask]) -> List[Landmark]:
    landmark_specs = [
        ("mask-vertebral-body-l4", "lm-l4-superior", "L4 superior endplate", "series-sag-t2", 58),
        ("mask-disc-l45", "lm-l4-l5-disc-midpoint", "L4-L5 disc midpoint", "series-sag-t2", 58),
        ("mask-canal-l45", "lm-canal-ap-l45", "L4-L5 canal AP diameter", "series-sag-t2", 58),
    ]
    landmarks: List[Landmark] = []
    for mask_id, landmark_id, label, series_id, slice_index in landmark_specs:
        mask = mask_by_id(masks, mask_id)
        if mask is not None:
            landmarks.append(landmark_from_mask(mask, landmark_id=landmark_id, label=label, series_id=series_id, slice_index=slice_index))
    return landmarks


def _measurement_from_mask(mask: Mask, *, measurement_id: str, label: str, level: str, axis: str, linked_landmarks: List[str]) -> Measurement:
    points = contour_points(mask, "series-sag-t2", 58)
    min_x, min_y, max_x, max_y = bounds(points)
    pixel_length = max_y - min_y if axis == "vertical" else max_x - min_x
    value = round(max(pixel_length, 0.0) * PIXEL_SPACING_MM, 1)
    return {
        "id": measurement_id,
        "label": label,
        "level": level,
        "value": value,
        "aiValue": value,
        "reviewerValue": None,
        "unit": "mm",
        "source": "AI",
        "confidence": float(mask.get("confidence", 0.72)),
        "status": "pendiente",
        "outlier": False,
        "linkedLandmarks": linked_landmarks,
    }


def build_measurements_from_contract(masks: List[Mask], landmarks: List[Landmark]) -> List[Measurement]:
    disc = mask_by_id(masks, "mask-disc-l45")
    canal = mask_by_id(masks, "mask-canal-l45")
    vertebral = mask_by_id(masks, "mask-vertebral-body-l4")
    measurements: List[Measurement] = []
    if disc is not None:
        measurements.append(_measurement_from_mask(disc, measurement_id="disc-height-l45", label="Disc height", level="L4-L5", axis="vertical", linked_landmarks=["lm-l4-l5-disc-midpoint"]))
    if canal is not None:
        measurements.append(_measurement_from_mask(canal, measurement_id="canal-diameter-l45", label="Central canal AP diameter", level="L4-L5", axis="horizontal", linked_landmarks=["lm-canal-ap-l45"]))
    if vertebral is not None:
        measurements.append(_measurement_from_mask(vertebral, measurement_id="vertebral-body-height-l4", label="Vertebral body height", level="L4", axis="vertical", linked_landmarks=["lm-l4-superior"]))
    return measurements


def contract_quality_summary(masks: List[Mask], landmarks: List[Landmark], measurements: List[Measurement]) -> Dict[str, Any]:
    confidences = [float(mask.get("confidence", 0.0)) for mask in masks]
    return {
        "maskCount": len(masks),
        "landmarkCount": len(landmarks),
        "measurementCount": len(measurements),
        "meanMaskConfidence": round(sum(confidences) / len(confidences), 3) if confidences else 0.0,
        "pixelSpacingMm": PIXEL_SPACING_MM,
        "measurementsDerivedFromContours": True,
    }
