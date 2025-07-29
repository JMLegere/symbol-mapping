"""FastAPI dependency providers."""

from .services.enrichment_service import EnrichmentService
from .services.ticker_service import TickerService


async def get_enrichment_service() -> EnrichmentService:
    """Return an ``EnrichmentService`` instance."""

    return EnrichmentService()


async def get_ticker_service() -> TickerService:
    """Return a ``TickerService`` instance."""

    return TickerService()
