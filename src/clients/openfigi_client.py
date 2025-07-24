from typing import List

import httpx

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry
from ..config import settings


class OpenFigiClient:
    BASE_URL = "https://api.openfigi.com/v3/mapping"

    def __init__(self) -> None:
        headers = {}
        if settings.openfigi_api_key:
            headers["X-OPENFIGI-APIKEY"] = settings.openfigi_api_key
        self._client = httpx.AsyncClient(headers=headers)

    async def close(self) -> None:
        await self._client.aclose()

    async def fetch_mappings(self, jobs: MappingRequest) -> List[MapEntry]:
        """Fetch FIGI mappings from the OpenFIGI service."""

        payload = [
            {"idType": f"ID_{job.idType}", "idValue": job.idValue}
            for job in jobs.jobs
        ]
        try:
            resp = await self._client.post(self.BASE_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:  # pragma: no cover - network errors
            return [
                MapEntry(
                    mappedIdType="FIGI",
                    mappedIdValue=None,
                    sources=[self.BASE_URL],
                    error=str(exc),
                )
            ]

        results: List[MapEntry] = []
        for item in data:
            if "data" not in item:
                results.append(
                    MapEntry(
                        mappedIdType="FIGI",
                        mappedIdValue=None,
                        sources=[self.BASE_URL],
                        error=item.get("error", "No mapping found"),
                    )
                )
                continue
            for entry in item["data"]:
                results.append(
                    MapEntry(
                        mappedIdType="FIGI",
                        mappedIdValue=entry.get("figi"),
                        sources=[self.BASE_URL],
                    )
                )

        return results
