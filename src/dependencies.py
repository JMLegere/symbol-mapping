"""FastAPI dependency providers."""

from .services.enrichment_service import EnrichmentService


async def get_enrichment_service() -> EnrichmentService:
    """Return an ``EnrichmentService`` instance."""

    return EnrichmentService()
