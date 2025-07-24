# Symbol Mapping

This project implements a small FastAPI service for symbol mapping.  It exposes
`POST /v1/mappings/{service}` where `{service}` is one of the predefined
mapping directions such as `cusip2figi` or `figi2isin`.

## Development

Install dependencies and run the application:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests with:

```bash
pytest
```
