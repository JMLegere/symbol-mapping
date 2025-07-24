from typing import List

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry


class MappingService:
    async def map(self, jobs: MappingRequest) -> List[MapEntry]:
        """Map identifiers."""
        # pragma: no cover - interface
        raise NotImplementedError
