from src.services.figi_service import OpenFigiService
from src.services.financedb_service import FinanceDbService
import pytest
from src.schemas.mapping_request import MappingJob, MappingRequest


@pytest.mark.asyncio
async def test_openfigi_service_mapping():
    service = OpenFigiService()
    jobs = MappingRequest(jobs=[
        MappingJob(idType="CUSIP", idValue="037833100")
    ])
    results = await service.map(jobs)
    assert results[0].mappedIdValue is not None
    assert "openfigi" in str(results[0].sources[0])


@pytest.mark.asyncio
async def test_financedb_service_mapping():
    service = FinanceDbService()
    jobs = MappingRequest(jobs=[
        MappingJob(idType="FIGI", idValue="BBG000B9XRY4")
    ])
    results = await service.map(jobs)
    assert results[0].mappedIdValue is not None
    assert "financedatabase" in str(results[0].sources[0])
