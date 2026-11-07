from app.config import settings
from app.exceptions import UnsupportedProviderError
from app.interfaces.detector_interface import FaceDetector


def get_detector() -> FaceDetector:
    if (detector := settings.detector) == "YuNet":
        from app.yunet_detector import YuNetFaceDetector

        return YuNetFaceDetector()
    if detector == "Media Pipe":
        from app.mediapipe_detector import MediaPipeFaceDetector

        return MediaPipeFaceDetector()
    raise UnsupportedProviderError(f"{detector} not supported")
