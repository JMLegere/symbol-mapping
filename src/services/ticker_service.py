from typing import List

from ..clients.openfigi_client import OpenFigiClient
from ..schemas.ticker_request import TickerRequest
from ..schemas.mapping_response import MapEntry
from ..utils.mic_mapping import mic_to_exch
from .base_service import MappingService


class TickerService(MappingService):
    """Map ticker and MIC to FIGI using OpenFIGI."""

    def __init__(self) -> None:
        self.client = OpenFigiClient()

    async def map(self, request: TickerRequest) -> List[MapEntry]:
        exch = mic_to_exch(request.mic)
        if not exch:
            return [self._error(f"Unknown MIC code: {request.mic}")]

        try:
            return await self.client.fetch_ticker_figi(request.ticker, exch)
        except Exception as exc:  # pragma: no cover - network errors
            return [self._error(str(exc))]

    def _error(self, message: str) -> MapEntry:
        return MapEntry(
            mappedIdType="FIGI",
            mappedIdValue=None,
            sources=[self.client.BASE_URL],
            error=message,
        )
