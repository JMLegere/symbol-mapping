from typing import Literal

from pydantic import BaseModel

AllowedIdType = Literal[
    "CUSIP",
    "ISIN",
    "FIGI",
    "FIGI_COMPOSITE",
    "FIGI_SHARE_CLASS",
]


class MappingRequest(BaseModel):
    """Request payload for a single identifier."""

    idType: AllowedIdType
    idValue: str
