"""Unit tests for shared frame decoding."""

from __future__ import annotations

import pytest

from app.frames import decode_frame
from app.interfaces.detector_interface import FrameDecodeError


def test_decode_frame_accepts_raw_base64(tiny_png_b64: str) -> None:
    arr = decode_frame(tiny_png_b64)
    assert arr.ndim == 3
    assert arr.shape[2] == 3
    assert arr.shape[0] == 1
    assert arr.shape[1] == 1


def test_decode_frame_accepts_data_url(tiny_png_data_url: str) -> None:
    arr = decode_frame(tiny_png_data_url)
    assert arr.shape == (1, 1, 3)


def test_decode_frame_accepts_rgb_png(rgb_png_b64: str) -> None:
    arr = decode_frame(rgb_png_b64)
    assert arr.shape == (4, 4, 3)


def test_decode_frame_rejects_invalid_base64() -> None:
    with pytest.raises(FrameDecodeError):
        decode_frame("%%%not-base64%%%")


def test_decode_frame_rejects_non_image_bytes() -> None:
    import base64

    payload = base64.b64encode(b"not-an-image").decode("ascii")
    with pytest.raises(FrameDecodeError):
        decode_frame(payload)
