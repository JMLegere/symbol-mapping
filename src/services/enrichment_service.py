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

    async def enrich(self, jobs: MappingRequest) -> List[MapEntry]:
        """Return mappings for the provided jobs."""
        results: List[MapEntry] = []
        for job in jobs.jobs:
            single = MappingRequest(jobs=[MappingJob(idType=job.idType, idValue=job.idValue)])
            if job.idType in {"CUSIP", "ISIN"}:
                results.extend(await self._figi.map(single))
            if job.idType == "FIGI":
                results.extend(await self._finance.map(single))
        return results
