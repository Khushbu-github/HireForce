from pydantic import BaseModel, Field


class DetectRequest(BaseModel):
    # One or more base64-encoded frames (JPEG/PNG; data-URL prefix tolerated).
    # Cap keeps a single request from flooding the detector threadpool.
    frames: list[str] = Field(min_length=1, max_length=8)
    # Checks to run. v1 supports only "face_count"; kept for forward-compat.
    checks: list[str] = Field(default_factory=lambda: ["face_count"])


class FaceBox(BaseModel):
    confidence: float
    x: int
    y: int
    width: int
    height: int


class DetectResponse(BaseModel):
    # Max faces across the submitted frames — conservative: a second person in
    # ANY frame trips the count.
    face_count: int
    # Per-frame counts, in request order.
    per_frame: list[int]
    # Boxes from the frame with the most faces (for evidence/debugging).
    faces: list[FaceBox] = Field(default_factory=list)


class HealthResponse(BaseModel):
    ok: bool
    ready: bool
    detector: str | None = None
    version: str = "0.1.0"
