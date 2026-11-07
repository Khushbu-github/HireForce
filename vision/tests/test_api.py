"""API tests for /health and /detect using a fake detector."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.schemas import FaceBox
from tests.conftest import FakeDetector


def test_health_reports_ready_detector(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["ready"] is True
    assert body["detector"]
    assert body["version"] == "0.1.0"


def test_detect_returns_face_count(
    client: TestClient, fake_detector: FakeDetector, tiny_png_b64: str
) -> None:
    response = client.post(
        "/detect",
        json={"frames": [tiny_png_b64], "checks": ["face_count"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["face_count"] == 1
    assert body["per_frame"] == [1]
    assert len(body["faces"]) == 1
    assert len(fake_detector.calls) == 1


def test_detect_uses_max_across_frames(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tiny_png_b64: str
) -> None:
    class VaryingDetector(FakeDetector):
        def count_faces(self, frame_b64: str) -> tuple[int, list[FaceBox]]:
            n = 1 if len(self.calls) == 0 else 2
            self.calls.append(frame_b64)
            boxes = [
                FaceBox(confidence=0.9, x=0, y=0, width=5, height=5) for _ in range(n)
            ]
            return n, boxes

    varying = VaryingDetector()
    monkeypatch.setattr("app.main._detector", varying)

    response = client.post(
        "/detect",
        json={"frames": [tiny_png_b64, tiny_png_b64], "checks": ["face_count"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["per_frame"] == [1, 2]
    assert body["face_count"] == 2


def test_detect_rejects_unknown_check(client: TestClient, tiny_png_b64: str) -> None:
    response = client.post(
        "/detect",
        json={"frames": [tiny_png_b64], "checks": ["pose"]},
    )
    assert response.status_code == 400
    assert "Unsupported checks" in response.json()["detail"]


def test_detect_rejects_bad_frame(client: TestClient) -> None:
    response = client.post(
        "/detect",
        json={"frames": ["bad-frame"], "checks": ["face_count"]},
    )
    assert response.status_code == 400
    assert "Bad frame" in response.json()["detail"]


def test_detect_requires_secret_when_configured(
    monkeypatch: pytest.MonkeyPatch, tiny_png_b64: str
) -> None:
    from app.main import app

    monkeypatch.setattr("app.main.get_detector", lambda: FakeDetector())
    monkeypatch.setattr("app.main.settings.shared_secret", "s3cret")

    with TestClient(app) as test_client:
        denied = test_client.post(
            "/detect",
            json={"frames": [tiny_png_b64], "checks": ["face_count"]},
        )
        assert denied.status_code == 401

        allowed = test_client.post(
            "/detect",
            headers={"X-Vision-Secret": "s3cret"},
            json={"frames": [tiny_png_b64], "checks": ["face_count"]},
        )
        assert allowed.status_code == 200
