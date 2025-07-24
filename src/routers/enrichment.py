from fastapi import APIRouter, Depends

from ..dependencies import get_enrichment_service
from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MappingResponse
from ..services.enrichment_service import EnrichmentService
from ..utils.merge_sources import merge_sources, prune_duplicates

router = APIRouter(prefix="/v1/enrich")


@router.post("", response_model=MappingResponse)
async def enrich(
    payload: MappingRequest,
    svc: EnrichmentService = Depends(get_enrichment_service),
) -> MappingResponse:
    raw = await svc.enrich(payload)
    merged = merge_sources(raw)
    return MappingResponse(results=prune_duplicates(merged))
