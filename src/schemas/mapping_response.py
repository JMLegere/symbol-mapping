from typing import List

from pydantic import BaseModel, HttpUrl


class MapEntry(BaseModel):
    mappedIdType: str
    mappedIdValue: str
    sources: List[HttpUrl]


class MappingResponse(BaseModel):
    results: List[MapEntry]
