from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.main import app  # noqa: E402


def main() -> int:
    current_schema = app.openapi()
    with open('api.yaml', 'r') as f:
        saved_schema = yaml.safe_load(f)
    if current_schema != saved_schema:
        print('OpenAPI schema mismatch. Please regenerate api.yaml')
        return 1
    print('OpenAPI schema matches api.yaml')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
