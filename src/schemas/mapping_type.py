from enum import Enum


class MappingType(str, Enum):
    cusip2figi = "cusip2figi"
    cusip2figicomposite = "cusip2figicomposite"
    cusip2figishareclass = "cusip2figishareclass"
    isin2figi = "isin2figi"
    isin2figicomposite = "isin2figicomposite"
    isin2figishareclass = "isin2figishareclass"
    figi2cusip = "figi2cusip"
    figi2isin = "figi2isin"
    figi2figicomposite = "figi2figicomposite"
    figi2figishareclass = "figi2figishareclass"
