import httpx

from app.config import settings
from app.schemas import PantryItemPayload


class PantryServiceError(RuntimeError):
    """Raised when the pantry service refuses to create an item."""


def create_pantry_item(payload: PantryItemPayload) -> dict:
    """POST to the pantry service `/items`.

    The URL comes from `PANTRY_INTERNAL_URL`, which already includes the API
    prefix (e.g. `http://pantry:8000/<envName>/pantry`).
    """
    url = f"{settings.pantry_internal_url.rstrip('/')}/items"
    try:
        response = httpx.post(
            url,
            json=payload.model_dump(exclude_none=True),
            timeout=settings.pantry_request_timeout_seconds,
        )
    except httpx.HTTPError as exc:
        raise PantryServiceError(f"pantry service unreachable: {exc}") from exc

    if response.status_code >= httpx.codes.BAD_REQUEST:
        raise PantryServiceError(f"pantry service returned {response.status_code}: {response.text}")
    return response.json()
