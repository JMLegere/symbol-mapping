from typing import List

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry


class FinanceDbClient:
    async def fetch_mappings(self, jobs: MappingRequest) -> List[MapEntry]:
        results: List[MapEntry] = []
        for job in jobs.jobs:
            results.append(
                MapEntry(
                    mappedIdType="TICKER",
                    mappedIdValue=f"FAKE-{job.idValue}",
                    sources=["https://finance.db"]
                )
            )
        return results
