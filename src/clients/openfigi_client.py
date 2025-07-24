from typing import Dict, Iterable, List

import httpx

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry
from ..config import settings

_MAPPING_FIELDS: Dict[str, str] = {
    "figi": "FIGI",
    "compositeFIGI": "FIGI_COMPOSITE",
    "shareClassFIGI": "FIGI_SHARE_CLASS",
    "isin": "ISIN",
    "cusip": "CUSIP",
}


class OpenFigiClient:
    """Client for the OpenFIGI mapping API."""

    BASE_URL = "https://api.openfigi.com/v3/mapping"

    _ID_MAP = {
        "CUSIP": "ID_CUSIP",
        "ISIN": "ID_ISIN",
        "FIGI": "ID_BB_GLOBAL",
    }

    def __init__(self) -> None:
        headers = {}
        if settings.openfigi_api_key:
            headers["X-OPENFIGI-APIKEY"] = settings.openfigi_api_key
        self._client = httpx.AsyncClient(headers=headers)

    async def close(self) -> None:
        await self._client.aclose()

    async def fetch_mappings(self, request: MappingRequest) -> List[MapEntry]:
        """Return all mappings related to the provided identifier."""
        api_type = self._ID_MAP.get(request.idType)
        if not api_type:
            return [
                MapEntry(
                    mappedIdType=request.idType,
                    mappedIdValue=None,
                    sources=[self.BASE_URL],
                    error=f"Unsupported idType: {request.idType}",
                )
            ]

        payload = [{"idType": api_type, "idValue": request.idValue}]
        try:
            resp = await self._client.post(self.BASE_URL, json=payload)
            resp.raise_for_status()
        except Exception as exc:  # pragma: no cover - network errors
            return [
                MapEntry(
                    mappedIdType=request.idType,
                    mappedIdValue=None,
                    sources=[self.BASE_URL],
                    error=str(exc),
                )
            ]

        data = resp.json()
        results: List[MapEntry] = []

        mapping_fields = _MAPPING_FIELDS

        for item in data:
            entries: Iterable[Dict[str, str]] | None = item.get("data")
            if not entries:
                results.append(
                    MapEntry(
                        mappedIdType=request.idType,
                        mappedIdValue=None,
                        sources=[self.BASE_URL],
                        error=item.get("error", "No mapping found"),
                    )
                )
                continue

            for entry in entries:
                for field, id_type in mapping_fields.items():
                    value = entry.get(field)
                    if not value or (
                        id_type == request.idType and value == request.idValue
                    ):
                        continue
                    results.append(
                        MapEntry(
                            mappedIdType=id_type,
                            mappedIdValue=value,
                            sources=[self.BASE_URL],
                        )
                    )

        return results
