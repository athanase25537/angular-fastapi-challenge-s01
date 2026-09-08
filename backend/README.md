## Run the API

From the repository root:

```bash
uv run --directory backend uvicorn main:app --reload --app-dir backend
```

The backend uses `DATABASE_URL` from `backend/.env`. If it is absent it starts
with a local SQLite database (`app.db`) so the frontend can be tried without a
PostgreSQL installation.

Set these values in `backend/.env` before a non-local deployment:

```env
DATABASE_URL=postgresql+psycopg://...
JWT_SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The API is available at `http://localhost:8000`, with interactive docs at
`http://localhost:8000/docs`. Authentication endpoints are:

- `POST /auth/register` — creates an account and returns a Bearer JWT.
- `POST /auth/login` — returns a Bearer JWT for an existing account.
- `GET /auth/me` — returns the current user and requires `Authorization: Bearer <token>`.

## Generate frontend DTOs

After changing a Pydantic request/response schema, regenerate the contract and
frontend types from the repository root:

```bash
PYTHONPATH=backend python -c "from main import app; from core.utils import export_openapi_to_json; from pathlib import Path; export_openapi_to_json(app, Path('openapi.json'))"
python DTOGenerator.py
```

Generated files live in `frontend/DTOGenerator/src/app/core/api/generated` and
are imported by the Angular API services as type-only imports.
