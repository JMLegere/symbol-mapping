from typing import List

import financedatabase as fd

from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry


class FinanceDbClient:
    """Client for the FinanceDatabase dataset."""

    def __init__(self) -> None:
        self._equities = fd.Equities().select()

    async def fetch_mappings(self, jobs: MappingRequest) -> List[MapEntry]:
        results: List[MapEntry] = []
        for job in jobs.jobs:
            df = self._equities[
                (self._equities["figi"] == job.idValue)
                | (self._equities["composite_figi"] == job.idValue)
                | (self._equities["shareclass_figi"] == job.idValue)
            ]
            if df.empty:
                results.append(
                    MapEntry(
                        mappedIdType="CUSIP",
                        mappedIdValue=None,
                        sources=["https://www.jeroenbouma.com/projects/financedatabase"],
                        error="No mapping found",
                    )
                )
                continue
            for _, row in df.iterrows():
                if row.get("cusip"):
                    results.append(
                        MapEntry(
                            mappedIdType="CUSIP",
                            mappedIdValue=str(row["cusip"]),
                            sources=["https://www.jeroenbouma.com/projects/financedatabase"],
                        )
                    )
                if row.get("isin"):
                    results.append(
                        MapEntry(
                            mappedIdType="ISIN",
                            mappedIdValue=str(row["isin"]),
                            sources=["https://www.jeroenbouma.com/projects/financedatabase"],
                        )
                    )
        return results
