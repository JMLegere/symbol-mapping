from fastapi import HTTPException

from .services.base_service import MappingService
from .services.figi_service import OpenFigiService
from .services.financedb_service import FinanceDbService
from .schemas.mapping_type import MappingType


async def get_mapping_service(service: MappingType) -> MappingService:
    """Resolve a service implementation based on the mapping type."""
    service_map: dict[MappingType, type[MappingService]] = {
        MappingType.cusip2figi: OpenFigiService,
        MappingType.cusip2figicomposite: OpenFigiService,
        MappingType.cusip2figishareclass: OpenFigiService,
        MappingType.isin2figi: OpenFigiService,
        MappingType.isin2figicomposite: OpenFigiService,
        MappingType.isin2figishareclass: OpenFigiService,
        MappingType.figi2cusip: FinanceDbService,
        MappingType.figi2isin: FinanceDbService,
        MappingType.figi2figicomposite: FinanceDbService,
        MappingType.figi2figishareclass: FinanceDbService,
    }

    service_cls = service_map.get(service)
    if not service_cls:
        raise HTTPException(status_code=400, detail="Unknown service")
    return service_cls()
