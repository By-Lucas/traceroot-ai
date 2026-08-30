# API

Interactive documentation is generated from FastAPI contracts:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Authentication

| Method | Path                    | Purpose                            |
| ------ | ----------------------- | ---------------------------------- |
| POST   | `/api/v1/auth/register` | Create user and isolated workspace |
| POST   | `/api/v1/auth/login`    | Issue access and refresh tokens    |
| POST   | `/api/v1/auth/refresh`  | Replace a valid token pair         |
| POST   | `/api/v1/auth/logout`   | Client-side token discard contract |
| GET    | `/api/v1/auth/me`       | Current user and workspace         |

Pass `Authorization: Bearer <access_token>` to protected routes.

## Domain routes

| Method   | Path                                     | Purpose                                     |
| -------- | ---------------------------------------- | ------------------------------------------- |
| POST/GET | `/api/v1/incidents`                      | Create/list owned incidents                 |
| GET      | `/api/v1/incidents/{id}`                 | Read an owned incident                      |
| POST     | `/api/v1/incidents/{id}/investigate`     | Execute the bounded workflow                |
| GET      | `/api/v1/investigations/{id}`            | Read state, hypotheses and evidence         |
| GET      | `/api/v1/investigations/{id}/trajectory` | Read observable stage trajectory            |
| GET      | `/api/v1/investigations/{id}/report`     | Read the structured final report            |
| POST/GET | `/api/v1/knowledge`                      | Ingest/list Markdown, TXT or JSON knowledge |
| POST     | `/api/v1/evaluations`                    | Execute the offline suite                   |
| GET      | `/api/v1/evaluations/{id}`               | Read evaluation result                      |

## Operations

`GET /health`, `GET /ready` and `GET /metrics` are unauthenticated operational endpoints. Error responses use `{"detail": "..."}` and retain a request ID response header.
