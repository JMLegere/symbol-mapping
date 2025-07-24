from typing import List

from pydantic import BaseModel, HttpUrl


class MapEntry(BaseModel):
    mappedIdType: str
    mappedIdValue: str | None = None
    sources: List[HttpUrl]
    error: str | None = None


class MappingResponse(BaseModel):
    results: List[MapEntry]
