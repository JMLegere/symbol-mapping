from typing import List

from ..clients.financedb_client import FinanceDbClient
from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry
from .base_service import MappingService


class FinanceDbService(MappingService):
    def __init__(self) -> None:
        self.client = FinanceDbClient()

    async def map(self, jobs: MappingRequest) -> List[MapEntry]:
        return await self.client.fetch_mappings(jobs)
