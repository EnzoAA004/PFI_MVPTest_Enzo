from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float


class MaskContour(BaseModel):
    series_id: str = Field(..., alias="seriesId")
    slice_index: int = Field(..., alias="sliceIndex")
    points: List[Point]


class StudySeries(BaseModel):
    id: str
    name: str
    plane: Literal["sagittal", "axial"]
    sequence: str
    slice_count: int = Field(..., alias="sliceCount")
    selected_slice: int = Field(..., alias="selectedSlice")
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    overlay_url: Optional[str] = Field(default=None, alias="overlayUrl")
    overlay_opacity: float = Field(default=0.74, alias="overlayOpacity")
    status: str = "ai_output_pending"


class StudyMask(BaseModel):
    id: str
    label: str
    class_name: str = Field(..., alias="className")
    color: str
    confidence: float
    editable: bool = True
    enabled: bool = True
    contours: List[MaskContour] = Field(default_factory=list)


class StudyLandmark(BaseModel):
    id: str
    label: str
    series_id: str = Field(..., alias="seriesId")
    slice_index: int = Field(..., alias="sliceIndex")
    x: float
    y: float
    editable: bool = True
    linked_mask_id: Optional[str] = Field(default=None, alias="linkedMaskId")


class StudyMeasurement(BaseModel):
    id: str
    label: str
    level: str
    value: float
    ai_value: float = Field(..., alias="aiValue")
    reviewer_value: Optional[float] = Field(default=None, alias="reviewerValue")
    unit: str
    source: Literal["AI", "Reviewer"] = "AI"
    confidence: float
    status: str = "pendiente"
    outlier: bool = False
    linked_landmarks: List[str] = Field(default_factory=list, alias="linkedLandmarks")


class AiOutputState(BaseModel):
    status: str
    label: str
    description: str
    real_inference_available: bool = Field(default=False, alias="realInferenceAvailable")
    human_review_required: bool = Field(default=True, alias="humanReviewRequired")
    not_clinical_diagnosis: bool = Field(default=True, alias="notClinicalDiagnosis")


class StudyReviewResponse(BaseModel):
    study_id: str = Field(..., alias="studyId")
    case_id: str = Field(..., alias="caseId")
    patient_id: str = Field(..., alias="patientId")
    study_date: str = Field(..., alias="studyDate")
    modality: str
    body_region: str = Field(..., alias="bodyRegion")
    review_status: str = Field(..., alias="reviewStatus")
    model_key: str = Field(..., alias="modelKey")
    model_version: str = Field(..., alias="modelVersion")
    ai_output: AiOutputState = Field(..., alias="aiOutput")
    series: List[StudySeries]
    masks: List[StudyMask]
    landmarks: List[StudyLandmark]
    measurements: List[StudyMeasurement]
    metadata: Dict[str, Any] = Field(default_factory=dict)


def demo_study_review_contract() -> Dict[str, Any]:
    response = StudyReviewResponse(
        studyId="STUDY-DEMO-0142",
        caseId="CASE-DEMO-0142",
        patientId="PAT-0087",
        studyDate="2026-07-01",
        modality="MRI",
        bodyRegion="Lumbar Spine",
        reviewStatus="pendiente",
        modelKey="sagittal_spider",
        modelVersion="contract-v1",
        aiOutput=AiOutputState(
            status="ai_output_pending",
            label="AI output pending / real inference pending",
            description="Prepared contract for overlayUrl, maskContours, landmarks and measurements.values.",
            realInferenceAvailable=False,
        ),
        series=[
            StudySeries(id="series-sag-t2", name="Sagittal T2", plane="sagittal", sequence="T2", sliceCount=96, selectedSlice=58),
            StudySeries(id="series-ax-t2", name="Axial T2 L4-L5", plane="axial", sequence="T2", sliceCount=48, selectedSlice=24),
        ],
        masks=[],
        landmarks=[],
        measurements=[
            StudyMeasurement(id="disc-height-l45", label="Disc Height", level="L4-L5", value=13.8, aiValue=13.8, unit="mm", confidence=0.82, linkedLandmarks=[]),
            StudyMeasurement(id="canal-diameter-l45", label="Central Canal Diameter", level="L4-L5", value=14.2, aiValue=14.2, unit="mm", confidence=0.76, linkedLandmarks=[]),
        ],
        metadata={"source": "ai-module-study-contract", "deidentified": True},
    )
    return response.model_dump(by_alias=True)
