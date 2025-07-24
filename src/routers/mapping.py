from fastapi import APIRouter, Depends

from ..dependencies import get_mapping_service
from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MappingResponse
from ..schemas.mapping_type import MappingType
from ..services.base_service import MappingService
from ..utils.merge_sources import merge_sources

router = APIRouter(prefix="/v1/mappings")


@router.post("/{service}", response_model=MappingResponse)
async def map_ids(
    service: MappingType,
    jobs: MappingRequest,
    svc: MappingService = Depends(get_mapping_service),
) -> MappingResponse:
    raw = await svc.map(jobs)
    return MappingResponse(results=merge_sources(raw))
