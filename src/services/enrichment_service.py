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

        if request.idType in {"CUSIP", "ISIN"}:
            figi_entries = await self._figi.map(request)
            results.extend(figi_entries)

            figi_values = [
                e.mappedIdValue for e in figi_entries if e.mappedIdValue
            ]
            for figi in figi_values:
                req = MappingRequest(idType="FIGI", idValue=figi)
                results.extend(await self._finance.map(req))
        elif request.idType == "FIGI":
            results.extend(await self._finance.map(request))

        return results
