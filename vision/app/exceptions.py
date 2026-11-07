from fastapi import status


class UnsupportedProviderError(Exception):
    def __init__(
        self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)


# Keep the old misspelling importable so any external callers don't break.
UnsuportedProviderError = UnsupportedProviderError
