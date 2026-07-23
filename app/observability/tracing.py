# app/observability/tracing.py
"""OpenTelemetry tracing setup for the RealEstate agent system.
Provides a single `init_tracing` function that configures:
- Console (stdout) exporter for quick local debugging.
- Optional OTLP exporter if `OTEL_EXPORTER_OTLP_ENDPOINT` env var is set.
- FastAPI middleware (`OpenTelemetryMiddleware`).
- Instrumentations for SQLAlchemy, Redis, Celery, and LiteLLM (via LangChain).
All instrumentations are imported lazily; missing packages are logged but do not raise.
"""

import os
import logging
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# FastAPI middleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Optional instrumentations – import inside functions to avoid hard dependency errors

def _instrument_sqlalchemy():
    try:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        # Base will be imported when the engine is created; we instrument globally
        SQLAlchemyInstrumentor().instrument(engine=None)
    except Exception as e:
        logging.getLogger(__name__).warning("SQLAlchemy instrumentation not available: %s", e)


def _instrument_redis():
    try:
        from opentelemetry.instrumentation.redis import RedisInstrumentor
        import redis  # Ensure redis is imported before instrumentation
        RedisInstrumentor().instrument()
    except Exception as e:
        logging.getLogger(__name__).warning("Redis instrumentation not available: %s", e)


def _instrument_celery():
    try:
        from opentelemetry.instrumentation.celery import CeleryInstrumentor
        from app.workers.celery_app import celery  # noqa: F401
        CeleryInstrumentor().instrument()
    except Exception as e:
        logging.getLogger(__name__).warning("Celery instrumentation not available: %s", e)


def _instrument_langchain():
    try:
        # LangChain respects LANGCHAIN_TRACING_V2 env var; no explicit instrumentation needed.
        pass
    except Exception as e:
        logging.getLogger(__name__).warning("LangChain instrumentation error: %s", e)


def init_tracing(app: Optional[object] = None) -> None:
    """Initialize OpenTelemetry tracing.

    - Configures a `TracerProvider` with a console exporter (default).
    - If `OTEL_EXPORTER_OTLP_ENDPOINT` is defined, adds an OTLP exporter.
    - Optionally instruments FastAPI (if ``app`` is provided), SQLAlchemy, Redis, Celery, and LangChain.
    """
    logger = logging.getLogger(__name__)

    provider = TracerProvider()
    # Console exporter for local dev
    console_exporter = ConsoleSpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(console_exporter))

    # OTLP exporter (optional) – read from environment
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        logger.info("OTLP exporter configured for OpenTelemetry: %s", otlp_endpoint)
    else:
        logger.info("OTLP exporter not configured; using console exporter only.")

    trace.set_tracer_provider(provider)

    # Apply instrumentations
    _instrument_sqlalchemy()
    _instrument_redis()
    _instrument_celery()
    _instrument_langchain()

    # FastAPI middleware – only if app instance is supplied
    if app is not None:
        FastAPIInstrumentor().instrument_app(app)
        logger.info("FastAPI OpenTelemetry instrumentation applied.")

    logger.info("OpenTelemetry tracing initialization complete.")
