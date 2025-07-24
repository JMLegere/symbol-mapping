from typing import List

from ..clients.openfigi_client import OpenFigiClient
from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry
from .base_service import MappingService


class OpenFigiService(MappingService):
    def __init__(self) -> None:
        self.client = OpenFigiClient()

    async def map(self, jobs: MappingRequest) -> List[MapEntry]:
        return await self.client.fetch_mappings(jobs)
