from src.services.figi_service import OpenFigiService
from src.services.financedb_service import FinanceDbService
import pytest
from src.schemas.mapping_request import MappingRequest


@pytest.mark.asyncio
async def test_openfigi_service_mapping():
    service = OpenFigiService()
    request = MappingRequest(idType="CUSIP", idValue="037833100")
    results = await service.map(request)
    assert results[0].mappedIdValue is not None
    assert "openfigi" in str(results[0].sources[0])


@pytest.mark.asyncio
async def test_financedb_service_mapping():
    service = FinanceDbService()
    request = MappingRequest(idType="FIGI", idValue="BBG000B9XRY4")
    results = await service.map(request)
    assert results[0].mappedIdValue is not None
    assert "financedatabase" in str(results[0].sources[0])
