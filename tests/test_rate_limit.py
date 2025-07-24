from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402
from src.main import create_app  # noqa: E402


def test_global_rate_limit() -> None:
    client = TestClient(create_app())
    payload = {"jobs": [{"idType": "CUSIP", "idValue": "12345678"}]}
    for _ in range(60):
        response = client.post("/v1/mappings/cusip2figi", json=payload)
        assert response.status_code == 200
    response = client.post("/v1/mappings/cusip2figi", json=payload)
    assert response.status_code == 429
