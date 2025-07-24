from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402
from src.main import create_app  # noqa: E402


def test_global_rate_limit() -> None:
    client = TestClient(create_app(max_requests=2, window_seconds=1000))
    payload = {"jobs": [{"idType": "CUSIP", "idValue": "037833100"}]}
    for _ in range(2):
        response = client.post("/v1/enrich", json=payload)
        assert response.status_code == 200
    response = client.post("/v1/enrich", json=payload)
    assert response.status_code == 429
