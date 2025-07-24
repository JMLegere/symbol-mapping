from typing import List

from ..schemas.mapping_response import MapEntry


def merge_sources(entries: List[MapEntry]) -> List[MapEntry]:
    merged: dict[tuple[str, str], MapEntry] = {}
    for entry in entries:
        key = (entry.mappedIdType, entry.mappedIdValue)
        if key not in merged:
            merged[key] = MapEntry(
                mappedIdType=entry.mappedIdType,
                mappedIdValue=entry.mappedIdValue,
                sources=list(entry.sources),
            )
        else:
            for src in entry.sources:
                if src not in merged[key].sources:
                    merged[key].sources.append(src)
    return list(merged.values())
