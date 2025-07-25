# Symbol Mapping

This project implements a small FastAPI service for identifier enrichment. It
exposes a single `POST /v1/enrich` endpoint that accepts an identifier payload
and returns mapped identifiers.

## Development

Install dependencies and run the application:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Run tests with:

```bash
pytest
```

## Deployment

The repository includes a `Procfile` for deployment on [Railway](https://railway.app/).
Railway automatically sets the `PORT` environment variable, so the application
can be started with:

```bash
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```
