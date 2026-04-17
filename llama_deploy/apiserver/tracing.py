"""Tracing utilities for llama_deploy."""

import logging
from contextlib import contextmanager, nullcontext
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Generator, TypeVar

if TYPE_CHECKING:
    from llama_deploy.apiserver.settings import ApiserverSettings


logger = logging.getLogger(__name__)

# Since opentelemetry is optional, we have to use Any to type the tracer
_tracer: Any | None = None
_tracing_enabled = False
_null_context = nullcontext()

F = TypeVar("F", bound=Callable[..., Any])


def configure_tracing(settings: "ApiserverSettings") -> None:
    """Configure OpenTelemetry tracing based on the provided configuration."""
    global _tracer, _tracing_enabled

    if not settings.tracing_enabled:
        logger.debug("Tracing is disabled")
        _tracing_enabled = False
        return

    try:
        from opentelemetry import trace
        from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

        # Create resource with service name
        resource = Resource.create({SERVICE_NAME: settings.tracing_service_name})

        # Create tracer provider with sampling
        tracer_provider = TracerProvider(
            resource=resource, sampler=TraceIdRatioBased(settings.tracing_sample_rate)
        )

        # Configure exporter based on config
        if settings.tracing_exporter == "console":
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter

            exporter = ConsoleSpanExporter()

        elif settings.tracing_exporter == "otlp":
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                OTLPSpanExporter,
            )

            if not settings.tracing_endpoint:
                raise ValueError("OTLP exporter requires an endpoint")
            exporter = OTLPSpanExporter(
                endpoint=f"{settings.tracing_endpoint}/v1/traces",
                insecure=settings.tracing_insecure,
                timeout=settings.tracing_timeout,
            )
        else:
            raise ValueError(f"Unsupported exporter: {settings.tracing_exporter}")

        # Add span processor
        span_processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(span_processor)

        # Set the global tracer provider
        trace.set_tracer_provider(tracer_provider)

        # Initialize global tracer
        _tracer = trace.get_tracer(__name__)
        _tracing_enabled = True

        # Setup auto-instrumentation
        AsyncioInstrumentor().instrument()

        logger.info(
            f"Tracing configured with {settings.tracing_exporter} exporter, service: {settings.tracing_service_name}"
        )

    except ImportError as e:
        msg = (
            f"Tracing is enabled but OpenTelemetry instrumentation packages are missing: {e}. "
            "Run `pip install llama_deploy[observability]`"
        )
        logger.warning(msg)
        _tracing_enabled = False
    except Exception as e:
        logger.error(f"Failed to configure tracing: {e}")
        _tracing_enabled = False


def get_tracer() -> Any | None:
    """Get the configured tracer instance."""
    pass


def is_tracing_enabled() -> bool:
    """Check if tracing is enabled."""
    pass


def trace_method(
    span_name: str | None = None, attributes: dict | None = None
) -> Callable[[F], F]:
    """Decorator to add tracing to synchronous methods."""
    pass


def trace_async_method(
    span_name: str | None = None, attributes: dict | None = None
) -> Callable[[F], F]:
    """Decorator to add tracing to asynchronous methods."""
    pass


@contextmanager
def create_span(
    name: str, attributes: dict | None = None
) -> Generator[Any, None, None]:
    pass


def add_span_attribute(key: str, value: Any) -> None:
    """Add an attribute to the current span if tracing is enabled."""
    pass


def add_span_event(name: str, attributes: dict | None = None) -> None:
    """Add an event to the current span if tracing is enabled."""
    pass
