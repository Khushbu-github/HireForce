"""Request schema validation tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas import DetectRequest


def test_detect_request_requires_at_least_one_frame() -> None:
    with pytest.raises(ValidationError):
        DetectRequest(frames=[])


def test_detect_request_caps_frames_at_eight(tiny_png_b64: str) -> None:
    with pytest.raises(ValidationError):
        DetectRequest(frames=[tiny_png_b64] * 9)


def test_detect_request_defaults_checks(tiny_png_b64: str) -> None:
    req = DetectRequest(frames=[tiny_png_b64])
    assert req.checks == ["face_count"]


def test_detect_request_accepts_eight_frames(tiny_png_b64: str) -> None:
    req = DetectRequest(frames=[tiny_png_b64] * 8)
    assert len(req.frames) == 8
