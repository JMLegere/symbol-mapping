from typing import List

import financedatabase as fd
from ..schemas.mapping_request import MappingRequest
from ..schemas.mapping_response import MapEntry


FINANCEDB_SOURCE = "https://www.jeroenbouma.com/projects/financedatabase"


class FinanceDbClient:
    """Client for the FinanceDatabase dataset."""

    def __init__(self) -> None:
        self._equities = fd.Equities().select()

    async def fetch_mappings(self, request: MappingRequest) -> List[MapEntry]:
        """Return mappings for the given identifier."""

        col_map = {
            "FIGI": "figi",
            "FIGI_COMPOSITE": "composite_figi",
            "FIGI_SHARE_CLASS": "shareclass_figi",
            "CUSIP": "cusip",
            "ISIN": "isin",
        }

        column = col_map.get(request.idType)
        if not column:
            return []

        search_cols = (
            [column]
            if request.idType != "FIGI"
            else ["figi", "composite_figi", "shareclass_figi"]
        )
        mask = False
        for col in search_cols:
            mask |= self._equities[col] == request.idValue
        df = self._equities[mask]
        if df.empty:
            return [
                MapEntry(
                    mappedIdType=request.idType,
                    mappedIdValue=None,
                    sources=[FINANCEDB_SOURCE],
                    error="No mapping found",
                )
            ]

        results: List[MapEntry] = []
        for _, row in df.iterrows():
            for key, col in col_map.items():
                if key == request.idType:
                    continue
                value = row.get(col)
                if value:
                    results.append(
                        MapEntry(
                            mappedIdType=key,
                            mappedIdValue=str(value),
                            sources=[FINANCEDB_SOURCE],
                        )
                    )
        return results
