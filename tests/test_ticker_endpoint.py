from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402
from src.main import create_app  # noqa: E402

client = TestClient(create_app())


def test_map_ticker_endpoint() -> None:
    payload = {"ticker": "AAPL", "mic": "XNAS"}
    response = client.post("/v1/mapticker", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["mappedIdValue"] is not None
