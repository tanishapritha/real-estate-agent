# app/observability/tracing.py
"""OpenTelemetry tracing setup for the RealEstate AI Sales OS.
This file provides a simple console exporter and a helper to instrument
FastAPI routes, SQLAlchemy engine, and background tasks.
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Initialize tracer provider with a console exporter (useful for dev)
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

def instrument_fastapi(app):
    """Instrument a FastAPI app for tracing.
    Call this during app initialization.
    """
    FastAPIInstrumentor.instrument_app(app)

def instrument_sqlalchemy(engine):
    """Instrument a SQLAlchemy engine.
    Pass the engine object after it is created.
    """
    SQLAlchemyInstrumentor().instrument(engine=engine)
