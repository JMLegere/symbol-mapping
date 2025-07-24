from __future__ import annotations

from typing import List

from ..schemas.mapping_request import MappingJob, MappingRequest
from ..schemas.mapping_response import MapEntry
from .figi_service import OpenFigiService
from .financedb_service import FinanceDbService


class EnrichmentService:
    """Aggregate enrichment from multiple mapping services."""

    def __init__(self) -> None:
        self._figi = OpenFigiService()
        self._finance = FinanceDbService()
        self._service_map = {
            "CUSIP": self._figi,
            "ISIN": self._figi,
            "FIGI": self._finance,
        }

    async def enrich(self, jobs: MappingRequest) -> List[MapEntry]:
        """Return mappings for each job using the appropriate service."""
        results: List[MapEntry] = []
        for job in jobs.jobs:
            service = self._service_map.get(job.idType)
            if not service:
                continue
            request = MappingRequest(
                jobs=[MappingJob(idType=job.idType, idValue=job.idValue)]
            )
            results.extend(await service.map(request))
        return results
