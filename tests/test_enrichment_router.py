from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402
from src.main import create_app  # noqa: E402

client = TestClient(create_app())


@pytest.mark.parametrize(
    "id_type,id_value",
    [
        ("CUSIP", "037833100"),  # Apple Inc.
        ("FIGI", "BBG000B9XRY4"),
    ],
)
def test_enrichment_router(id_type: str, id_value: str) -> None:
    payload = {"jobs": [{"idType": id_type, "idValue": id_value}]}
    response = client.post("/v1/enrich", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]["mappedIdValue"] is not None
