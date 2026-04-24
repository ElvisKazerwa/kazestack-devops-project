"""
Production-ready Flask application with Prometheus metrics, structured logging, and health checks.

This application demonstrates cloud-native best practices:
- Structured JSON logging for centralized aggregation
- Prometheus metrics for monitoring and alerting
- Health check endpoints for Kubernetes probes
- Graceful error handling and request tracking
"""

import logging
import time
import json
import sys
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, Gauge
import os

# ============================================================================
# Application Setup
# ============================================================================

app = Flask(__name__)

# ============================================================================
# Structured Logging Configuration
# ============================================================================


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

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

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


# Configure logging
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(JSONFormatter())
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

# ============================================================================
# Prometheus Metrics
# ============================================================================

# Request metrics
REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0),
)

# Error metrics
ERROR_COUNT = Counter(
    "app_errors_total", "Total application errors", ["error_type", "endpoint"]
)

# Application metrics
APP_INFO = Gauge("app_info", "Application information", ["version", "environment"])

# Active connections
ACTIVE_CONNECTIONS = Gauge("app_active_connections", "Number of active connections")

# ============================================================================
# Middleware & Decorators
# ============================================================================


@app.before_request
def before_request():
    """Record request start time and increment active connections"""
    request.start_time = time.time()
    ACTIVE_CONNECTIONS.inc()
    request.request_id = request.headers.get("X-Request-ID", str(time.time()))


@app.after_request
def after_request(response):
    """Record request metrics and decrement active connections"""
    if hasattr(request, "start_time"):
        duration = time.time() - request.start_time
        endpoint = request.endpoint or "unknown"

        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method, endpoint=endpoint, status=response.status_code
        ).inc()

        REQUEST_DURATION.labels(method=request.method, endpoint=endpoint).observe(
            duration
        )

        # Log request
        logger.info(
            f"Request completed",
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


@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    endpoint = request.endpoint or "unknown"
    error_type = type(error).__name__

    ERROR_COUNT.labels(error_type=error_type, endpoint=endpoint).inc()

    logger.error(
        f"Request failed: {str(error)}",
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


# ============================================================================
# API Endpoints
# ============================================================================


@app.route("/", methods=["GET"])
def hello():
    """Main endpoint - returns application information"""
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
    """Application status endpoint"""
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
    """Application information endpoint"""
    return (
        jsonify(
            {
                "app_name": "Kazestack K8s App",
                "version": "1.0.0",
                "environment": os.environ.get("FLASK_ENV", "production"),
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


# ============================================================================
# Health Check Endpoints (Kubernetes Probes)
# ============================================================================


@app.route("/health", methods=["GET"])
def liveness_probe():
    """
    Liveness probe for Kubernetes
    Returns 200 if application is running and responsive
    """
    return (
        jsonify({"status": "alive", "timestamp": datetime.utcnow().isoformat() + "Z"}),
        200,
    )


@app.route("/ready", methods=["GET"])
def readiness_probe():
    """
    Readiness probe for Kubernetes
    Returns 200 if application is ready to accept traffic
    """
    # Add any dependency checks here (e.g., database, cache)
    try:
        return (
            jsonify(
                {"status": "ready", "timestamp": datetime.utcnow().isoformat() + "Z"}
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}", exc_info=True)
        return (
            jsonify(
                {
                    "status": "not_ready",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            ),
            503,
        )


# ============================================================================
# Metrics Endpoints
# ============================================================================


@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Prometheus metrics endpoint
    Exposes all application and system metrics
    """
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}


# ============================================================================
# Application Startup
# ============================================================================


def initialize_app():
    """Initialize application metrics and logging"""
    environment = os.environ.get("FLASK_ENV", "production")
    version = "1.0.0"

    # Set app info gauge
    APP_INFO.labels(version=version, environment=environment).set(1)

    logger.info(
        f"Application initialized",
        extra={
            "app_name": "k8s-app",
            "version": version,
            "environment": environment,
            "port": os.environ.get("PORT", "5000"),
        },
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    initialize_app()

    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        use_reloader=False,  # Disable reloader in containers
    )
