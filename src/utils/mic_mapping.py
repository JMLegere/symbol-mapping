"""Mapping utilities for MIC to FIGI exchange codes."""

MIC_TO_EXCH = {
    "XNAS": "US",  # NASDAQ
    "XNYS": "US",  # New York Stock Exchange
    "ARCX": "US",  # NYSE Arca
    "XASE": "US",  # NYSE American
    "XLON": "LN",  # London Stock Exchange
}


def mic_to_exch(mic: str) -> str | None:
    """Return the FIGI exchange code for a MIC code if known."""
    return MIC_TO_EXCH.get(mic.upper())
