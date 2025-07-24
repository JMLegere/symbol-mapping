from __future__ import annotations

from typing import List

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry
from .figi_service import OpenFigiService
from .financedb_service import FinanceDbService


class EnrichmentService:
    """Aggregate enrichment from multiple mapping services."""

    def __init__(self) -> None:
        self._figi = OpenFigiService()
        self._finance = FinanceDbService()

    async def enrich(self, request: MappingRequest) -> List[MapEntry]:
        """Return mappings gathered from all configured services."""

        results: List[MapEntry] = []

        results.extend(await self._figi.map(request))
        results.extend(await self._finance.map(request))

        return results
