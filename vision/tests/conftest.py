"""Shared fixtures for the HireForce vision test suite."""

from __future__ import annotations

import base64
import io
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.interfaces.detector_interface import FaceDetector, FrameDecodeError
from app.schemas import FaceBox


# 1x1 PNG — valid image bytes for decode / detect smoke paths.
TINY_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class FakeDetector(FaceDetector):
    """Deterministic detector so API tests never load YuNet/MediaPipe."""

    def __init__(self, face_count: int = 1) -> None:
        self.face_count = face_count
        self.calls: list[str] = []

    def count_faces(self, frame_b64: str) -> tuple[int, list[FaceBox]]:
        self.calls.append(frame_b64)
        if frame_b64 == "bad-frame":
            raise FrameDecodeError("not an image")
        boxes = [
            FaceBox(confidence=0.99, x=1, y=2, width=10, height=12)
            for _ in range(self.face_count)
        ]
        return self.face_count, boxes


@pytest.fixture
def tiny_png_b64() -> str:
    return TINY_PNG_B64


@pytest.fixture
def tiny_png_data_url(tiny_png_b64: str) -> str:
    return f"data:image/png;base64,{tiny_png_b64}"


@pytest.fixture
def rgb_png_b64() -> str:
    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color=(12, 34, 56)).save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


@pytest.fixture
def fake_detector() -> FakeDetector:
    return FakeDetector(face_count=1)


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, fake_detector: FakeDetector) -> Iterator[TestClient]:
    monkeypatch.setattr("app.main.get_detector", lambda: fake_detector)
    monkeypatch.setattr("app.main.settings.shared_secret", "")
    # Import after patch target exists; lifespan will call the patched factory.
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
