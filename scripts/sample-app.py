#!/usr/bin/env python3
"""
Sample Application with OpenTelemetry Integration
Demonstrates real metrics, logs, and traces
"""

import time
import random
import logging
from opentelemetry import trace, metrics, logs
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.logs import LoggerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingHandler

# Configure OpenTelemetry
resource = Resource.create({
    "service.name": "sample-app",
    "service.version": "1.0.0",
    "environment": "demo"
})

# Set up tracing
trace.set_tracer_provider(
    TracerProvider(resource=resource)
)
tracer = trace.get_tracer(__name__)

# Set up metrics
metric_reader = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
metrics.set_meter_provider(
    MeterProvider(resource=resource)
)
meter = metrics.get_meter(__name__)

# Set up logging
log_exporter = OTLPLogExporter(endpoint="http://localhost:4317", insecure=True)
logs.set_logger_provider(
    LoggerProvider(resource=resource, log_exporter=log_exporter)
)
logger = logs.get_logger(__name__)

# Create metrics
request_counter = meter.create_counter("http_requests_total", description="Total HTTP requests")
request_duration = meter.create_histogram("http_request_duration_seconds", description="HTTP request duration")

# Instrument requests
RequestsInstrumentor().instrument()

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO))

def simulate_api_request():
    """Simulate an API request with telemetry"""
    
    with tracer.start_as_current_span("api-request") as span:
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", "/api/users")
        span.set_attribute("http.status_code", 200)
        
        start_time = time.time()
        
        # Simulate work
        time.sleep(random.uniform(0.1, 0.5))
        
        # Record metric
        request_duration.record(time.time() - start_time, {"method": "GET", "status": "200"})
        request_counter.add(1, {"method": "GET", "status": "200"})
        
        # Log the request
        logger.info("API request processed", 
                  attributes={
                      "http.method": "GET",
                      "http.status_code": 200,
                      "user.id": f"user_{random.randint(1000, 9999)}",
                      "request.duration_ms": int((time.time() - start_time) * 1000)
                  })
        
        # Simulate occasional errors
        if random.random() < 0.1:  # 10% error rate
            span.set_attribute("http.status_code", 500)
            request_counter.add(1, {"method": "GET", "status": "500"})
            logger.error("API request failed", 
                       attributes={
                           "http.method": "GET",
                           "http.status_code": 500,
                           "error.type": "database_timeout"
                       })
            return 500
        
        return 200

if __name__ == "__main__":
    logger.info("Sample application starting", 
              attributes={
                  "service.name": "sample-app",
                  "service.version": "1.0.0"
              })
    
    while True:
        simulate_api_request()
        time.sleep(random.uniform(1, 3))
