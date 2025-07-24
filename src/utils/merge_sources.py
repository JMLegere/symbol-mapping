"""Utilities for manipulating mapping entries."""

from typing import Iterable, List

from ..schemas.mapping_response import MapEntry


def prune_duplicates(entries: Iterable[MapEntry]) -> List[MapEntry]:
    """Remove entries that are identical in all fields."""

    unique: list[MapEntry] = []
    seen: set[tuple[str, str | None, tuple[str, ...], str | None]] = set()

    for entry in entries:
        key = (
            entry.mappedIdType,
            entry.mappedIdValue,
            tuple(entry.sources),
            entry.error,
        )
        if key not in seen:
            seen.add(key)
            unique.append(entry)

    return unique


def merge_sources(entries: Iterable[MapEntry]) -> List[MapEntry]:
    """Merge source URLs for entries with the same type and value."""

    merged: dict[tuple[str, str], MapEntry] = {}
    others: list[MapEntry] = []

    for entry in entries:
        if entry.mappedIdValue is None:
            others.append(entry)
            continue

        key = (entry.mappedIdType, entry.mappedIdValue)
        result = merged.get(key)
        if not result:
            result = merged[key] = MapEntry(
                mappedIdType=entry.mappedIdType,
                mappedIdValue=entry.mappedIdValue,
                sources=list(entry.sources),
            )
        else:
            for src in entry.sources:
                if src not in result.sources:
                    result.sources.append(src)

    return list(merged.values()) + others
