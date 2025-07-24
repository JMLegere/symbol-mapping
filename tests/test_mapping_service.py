from src.services.figi_service import OpenFigiService
from src.services.financedb_service import FinanceDbService
import pytest
from src.schemas.mapping_request import MappingJob, MappingRequest


@pytest.mark.asyncio
async def test_openfigi_service_mapping():
    service = OpenFigiService()
    jobs = MappingRequest(jobs=[
        MappingJob(idType="CUSIP", idValue="12345678")
    ])
    results = await service.map(jobs)
    assert results[0].mappedIdValue == "FAKE-12345678"
    assert str(results[0].sources[0]) == "https://openfigi.com/"


@pytest.mark.asyncio
async def test_financedb_service_mapping():
    service = FinanceDbService()
    jobs = MappingRequest(jobs=[
        MappingJob(idType="CUSIP", idValue="87654321")
    ])
    results = await service.map(jobs)
    assert results[0].mappedIdValue == "FAKE-87654321"
    assert str(results[0].sources[0]) == "https://finance.db/"
