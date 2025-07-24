from typing import List

import financedatabase as fd
from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry


FINANCEDB_SOURCE = "https://www.jeroenbouma.com/projects/financedatabase"


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
                        sources=[FINANCEDB_SOURCE],
                        error="No mapping found",
                    )
                )
                continue

            filtered = df[["cusip", "isin"]].dropna(how="all")
            for cusip, isin in filtered.itertuples(index=False):
                if cusip:
                    results.append(
                        MapEntry(
                            mappedIdType="CUSIP",
                            mappedIdValue=str(cusip),
                            sources=[FINANCEDB_SOURCE],
                        )
                    )
                if isin:
                    results.append(
                        MapEntry(
                            mappedIdType="ISIN",
                            mappedIdValue=str(isin),
                            sources=[FINANCEDB_SOURCE],
                        )
                    )

        return results
