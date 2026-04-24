"""
Production-ready Flask application with Prometheus metrics, structured logging,
health checks, and Kubernetes readiness/liveness probes.

Features:
- Structured JSON logging
- Prometheus metrics
- Kubernetes health probes
- Request telemetry
- Global error handling
"""

import json
import logging
import os
import sys
import time
from datetime import datetime

from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge, Histogram, generate_latest

# =============================================================================
# Flask App
# =============================================================================

app = Flask(__name__)

# =============================================================================
# Structured Logging
# =============================================================================


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(JSONFormatter())

app.logger.handlers.clear()
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.handlers.clear()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# =============================================================================
# Prometheus Metrics
# =============================================================================

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005,0.01,0.025,0.05,0.075,0.1,0.25,0.5,0.75,1.0,2.5,5.0,
    ),
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total application errors",
    ["error_type", "endpoint"],
)

APP_INFO = Gauge(
    "app_info",
    "Application information",
    ["version", "environment"],
)

ACTIVE_CONNECTIONS = Gauge(
    "app_active_connections",
    "Current active connections",
)

# =============================================================================
# Request Hooks
# =============================================================================


@app.before_request
def before_request():
    """Track request start and active connections."""
    request.start_time = time.time()
    request.request_id = request.headers.get(
        "X-Request-ID",
        str(time.time()),
    )
    ACTIVE_CONNECTIONS.inc()


@app.after_request
def after_request(response):
    """Collect metrics and log request details."""
    if hasattr(request, "start_time"):
        duration = time.time() - request.start_time
        endpoint = request.endpoint or "unknown"

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code,
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

        logger.info(
            "Request completed",
            extra={
                "request_id": request.request_id,
                "method": request.method,
                "endpoint": endpoint,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round(duration * 1000, 2),
                "remote_addr": request.remote_addr,
            },
        )

    ACTIVE_CONNECTIONS.dec()
    return response


# =============================================================================
# Error Handling
# =============================================================================


@app.errorhandler(Exception)
def handle_error(error):
    """Global exception handler."""
    endpoint = request.endpoint or "unknown"
    error_type = type(error).__name__

    ERROR_COUNT.labels(
        error_type=error_type,
        endpoint=endpoint,
    ).inc()

    logger.error(
        "Request failed: %s",
        error,
        extra={
            "request_id": getattr(request, "request_id", "unknown"),
            "error_type": error_type,
            "endpoint": endpoint,
        },
        exc_info=True,
    )

    return (
        jsonify(
            {
                "error": "Internal server error",
                "request_id": getattr(request, "request_id", "unknown"),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ),
        500,
    )


# =============================================================================
# API Endpoints
# =============================================================================


@app.route("/", methods=["GET"])
def hello():
    return (
        jsonify(
            {
                "message": "Hello from Kubernetes!",
                "version": "1.0.0",
                "status": "running",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ),
        200,
    )


@app.route("/api/status", methods=["GET"])
def status():
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "k8s-app",
                "version": "1.0.0",
                "uptime_seconds": int(time.time()),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ),
        200,
    )


@app.route("/api/info", methods=["GET"])
def info():
    return (
        jsonify(
            {
                "app_name": "Kazestack K8s App",
                "version": "1.0.0",
                "environment": os.environ.get(
                    "FLASK_ENV",
                    "production",
                ),
                "endpoints": [
                    "/",
                    "/api/status",
                    "/api/info",
                    "/health",
                    "/ready",
                    "/metrics",
                ],
            }
        ),
        200,
    )


# =============================================================================
# Kubernetes Probes
# =============================================================================


@app.route("/health", methods=["GET"])
def liveness_probe():
    return (
        jsonify(
            {
                "status": "alive",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ),
        200,
    )


@app.route("/ready", methods=["GET"])
def readiness_probe():
    try:
        return (
            jsonify(
                {
                    "status": "ready",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            ),
            200,
        )

    except Exception as exc:
        logger.error(
            "Readiness check failed: %s",
            exc,
            exc_info=True,
        )

        return (
            jsonify(
                {
                    "status": "not_ready",
                    "error": str(exc),
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            ),
            503,
        )


# =============================================================================
# Prometheus Metrics Endpoint
# =============================================================================


@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; charset=utf-8"
    }


# =============================================================================
# Startup
# =============================================================================


def initialize_app():
    """Initialize app metadata."""
    environment = os.environ.get("FLASK_ENV", "production")
    version = "1.0.0"

    APP_INFO.labels(
        version=version,
        environment=environment,
    ).set(1)

    logger.info(
        "Application initialized",
        extra={
            "app_name": "k8s-app",
            "version": version,
            "environment": environment,
            "port": os.environ.get("PORT", "5000"),
        },
    )


# =============================================================================
# Entrypoint
# =============================================================================

if __name__ == "__main__":
    initialize_app()

    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        use_reloader=False,
    )