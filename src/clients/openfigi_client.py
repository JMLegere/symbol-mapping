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

    async def _post(self, payload: List[dict]) -> List[dict]:
        resp = await self._client.post(self.BASE_URL, json=payload)
        resp.raise_for_status()
        return resp.json()

    async def _parse(
        self, data: List[dict], request_type: str, request_value: str
    ) -> List[MapEntry]:
        results: List[MapEntry] = []
        for item in data:
            entries: Iterable[Dict[str, str]] | None = item.get("data")
            if not entries:
                results.append(
                    MapEntry(
                        mappedIdType=request_type,
                        mappedIdValue=None,
                        sources=[self.BASE_URL],
                        error=item.get("error", "No mapping found"),
                    )
                )
                continue
            for entry in entries:
                for field, id_type in _MAPPING_FIELDS.items():
                    value = entry.get(field)
                    if not value or (
                        id_type == request_type and value == request_value
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
            data = await self._post(payload)
        except Exception as exc:  # pragma: no cover - network errors
            return [
                MapEntry(
                    mappedIdType=request.idType,
                    mappedIdValue=None,
                    sources=[self.BASE_URL],
                    error=str(exc),
                )
            ]

        return await self._parse(data, request.idType, request.idValue)

    async def fetch_ticker_figi(
        self, ticker: str, exch_code: str
    ) -> List[MapEntry]:
        payload = [
            {"idType": "TICKER", "idValue": ticker, "exchCode": exch_code}
        ]
        data = await self._post(payload)
        return await self._parse(data, "FIGI", ticker)
