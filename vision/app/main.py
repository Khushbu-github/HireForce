import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, status

from app.config import settings
from app.interfaces.detector_interface import FaceDetector, FrameDecodeError
from app.schemas import DetectRequest, DetectResponse, FaceBox, HealthResponse
from app.utils import get_detector

_SUPPORTED_CHECKS = frozenset({"face_count"})
_detector: FaceDetector | None = None
_detector_name: str | None = None
_startup_error: str | None = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    global _detector, _detector_name, _startup_error
    try:
        _detector = get_detector()
        _detector_name = settings.detector
        _startup_error = None
    except Exception as exc:  # noqa: BLE001 — surface any init failure via /health
        _detector = None
        _detector_name = settings.detector
        _startup_error = str(exc)
    yield
    _detector = None
    _detector_name = None
    _startup_error = None


app = FastAPI(title="HireForce Vision", version="0.1.0", lifespan=lifespan)


async def require_secret(x_vision_secret: str | None = Header(default=None)) -> None:
    if settings.shared_secret and x_vision_secret != settings.shared_secret:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid vision secret")


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    ready = _detector is not None
    return HealthResponse(
        ok=ready,
        ready=ready,
        detector=_detector_name if ready else None,
    )


@app.post("/detect", response_model=DetectResponse, dependencies=[Depends(require_secret)])
async def detect(req: DetectRequest) -> DetectResponse:
    detector = _detector
    if detector is None:
        detail = "Detector not ready"
        if _startup_error:
            detail = f"{detail}: {_startup_error}"
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail)

    unknown = [check for check in req.checks if check not in _SUPPORTED_CHECKS]
    if unknown:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Unsupported checks: {', '.join(unknown)}. Supported: face_count",
        )

    def run() -> tuple[list[int], list[FaceBox]]:
        counts: list[int] = []
        best: list[FaceBox] = []
        for frame in req.frames:
            n, boxes = detector.count_faces(frame)
            counts.append(n)
            if n >= len(best):
                best = boxes
        return counts, best

    try:
        per_frame, faces = await asyncio.to_thread(run)
    except FrameDecodeError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Bad frame: {exc}") from exc

    return DetectResponse(
        face_count=max(per_frame) if per_frame else 0,
        per_frame=per_frame,
        faces=faces,
    )
