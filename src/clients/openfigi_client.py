from typing import List

import httpx

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry


class OpenFigiClient:
    BASE_URL = "https://api.openfigi.com/v3/mapping"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient()

    async def close(self) -> None:
        await self._client.aclose()

    async def fetch_mappings(self, jobs: MappingRequest) -> List[MapEntry]:
        # Minimal placeholder implementation
        # Would normally call the OpenFIGI API
        results: List[MapEntry] = []
        for job in jobs.jobs:
            results.append(
                MapEntry(
                    mappedIdType="FIGI",
                    mappedIdValue=f"FAKE-{job.idValue}",
                    sources=["https://openfigi.com"]
                )
            )
        return results
