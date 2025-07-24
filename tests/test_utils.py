from src.schemas.mapping_response import MapEntry
from src.utils.merge_sources import merge_sources, prune_duplicates


def test_prune_duplicates():
    entries = [
        MapEntry(
            mappedIdType="CUSIP",
            mappedIdValue="1",
            sources=["http://a.com"],
        ),
        MapEntry(
            mappedIdType="CUSIP",
            mappedIdValue="1",
            sources=["http://a.com"],
        ),
        MapEntry(
            mappedIdType="CUSIP",
            mappedIdValue="1",
            sources=["http://b.com"],
        ),
    ]

    merged = merge_sources(entries)
    unique = prune_duplicates(merged)

    assert len(unique) == 1
    assert {str(url) for url in unique[0].sources} == {
        "http://a.com/",
        "http://b.com/",
    }
