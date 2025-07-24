from typing import List, Literal

from pydantic import BaseModel

AllowedIdType = Literal[
    "CUSIP",
    "ISIN",
    "FIGI",
    "FIGI_COMPOSITE",
    "FIGI_SHARE_CLASS",
]


class MappingJob(BaseModel):
    idType: AllowedIdType
    idValue: str


class MappingRequest(BaseModel):
    jobs: List[MappingJob]
