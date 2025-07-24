from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402
from src.main import app  # noqa: E402

client = TestClient(app)


@pytest.mark.parametrize(
    "service,id_type,id_value",
    [
        ("cusip2figi", "CUSIP", "12345678"),
        ("figi2cusip", "FIGI", "BBG000CL9VN4"),
    ],
)
def test_mapping_router(service: str, id_type: str, id_value: str) -> None:
    payload = {"jobs": [{"idType": id_type, "idValue": id_value}]}
    response = client.post(f"/v1/mappings/{service}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]["mappedIdValue"] == f"FAKE-{id_value}"
