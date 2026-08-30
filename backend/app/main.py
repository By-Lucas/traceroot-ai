import logging
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import text

from app.api.routes import auth, evaluations, incidents, investigations, knowledge
from app.core.config import get_settings
from app.core.errors import TraceRootError
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.observability.logging import configure_logging, request_id_var

settings = get_settings()
REQUEST_COUNT = Counter(
    "traceroot_http_requests_total", "HTTP requests", ["method", "path", "status"]
)
REQUEST_DURATION = Histogram(
    "traceroot_http_request_duration_seconds", "HTTP request latency", ["method", "path"]
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    if settings.app_env in {"development", "test"}:
        Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="TraceRoot API",
    version="0.1.0",
    description="Evidence-first agentic production incident investigation.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))[:128]
    token = request_id_var.set(request_id)
    started = time.perf_counter()
    try:
        response = await call_next(request)
        duration = time.perf_counter() - started
        path = request.url.path
        REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
        REQUEST_DURATION.labels(request.method, path).observe(duration)
        response.headers["x-request-id"] = request_id
        logging.info(
            "request completed",
            extra={"duration_ms": int(duration * 1000), "status": response.status_code},
        )
        return response
    finally:
        request_id_var.reset(token)


@app.exception_handler(TraceRootError)
async def domain_error(_: Request, exc: TraceRootError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc), "type": type(exc).__name__})


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "traceroot-api"}


@app.get("/ready", tags=["operations"])
def ready() -> dict[str, str]:
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    return {"status": "ready", "database": "connected"}


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


for route in (
    auth.router,
    incidents.router,
    investigations.router,
    knowledge.router,
    evaluations.router,
):
    app.include_router(route, prefix="/api/v1")
