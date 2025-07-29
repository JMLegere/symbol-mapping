from __future__ import annotations

from fastapi import APIRouter, Depends

from ..schemas.ticker_request import TickerRequest
from ..schemas.mapping_response import MapEntry
from ..services.ticker_service import TickerService
from ..dependencies import get_ticker_service

router = APIRouter(prefix="/v1/mapticker")


@router.post("", response_model=list[MapEntry])
async def map_ticker(
    payload: TickerRequest,
    service: TickerService = Depends(get_ticker_service),
) -> list[MapEntry]:
    """Map ticker/MIC pair to FIGI."""
    return await service.map(payload)
