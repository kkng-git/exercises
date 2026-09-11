import json
import logging
import os
import random
import time
import uuid
from datetime import datetime, timezone

import psycopg2
from datadog.dogstatsd import DogStatsd
from ddtrace import tracer
from flask import Flask, g, jsonify, request


app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")
DD_AGENT_HOST = os.getenv("DD_AGENT_HOST", "127.0.0.1")
DD_DOGSTATSD_PORT = int(os.getenv("DD_DOGSTATSD_PORT", "8125"))
DD_ENV = os.getenv("DD_ENV", "lab")
DD_SERVICE = os.getenv("DD_SERVICE", "three-tier-api")
DD_VERSION = os.getenv("DD_VERSION", "v2")
SLOW_MIN_SECONDS = float(os.getenv("SLOW_MIN_SECONDS", "0.8"))
SLOW_MAX_SECONDS = float(os.getenv("SLOW_MAX_SECONDS", "1.8"))

statsd = DogStatsd(
    host=DD_AGENT_HOST,
    port=DD_DOGSTATSD_PORT,
    namespace="three_tier",
    constant_tags=[f"env:{DD_ENV}", f"service:{DD_SERVICE}", f"version:{DD_VERSION}"],
)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "dd.env": getattr(record, "dd.env", DD_ENV),
            "dd.service": getattr(record, "dd.service", DD_SERVICE),
            "dd.version": getattr(record, "dd.version", DD_VERSION),
            "dd.trace_id": getattr(record, "dd.trace_id", "0"),
            "dd.span_id": getattr(record, "dd.span_id", "0"),
        }
        for field in ("request_id", "scenario", "status_code", "duration_ms"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("three-tier-api")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


class SimulatedFailure(RuntimeError):
    pass


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )


def check_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()


def init_db():
    for attempt in range(1, 11):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL
                        );
                        """
                    )
            logger.info("Database initialized")
            return
        except Exception:
            logger.warning("Waiting for database", extra={"attempt": attempt}, exc_info=True)
            time.sleep(2)
    raise RuntimeError("Database was not ready after 10 attempts")


def route_name():
    return request.url_rule.rule if request.url_rule else request.path


@app.before_request
def start_request():
    g.started_at = time.perf_counter()
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.scenario = "none"


@app.after_request
def observe_request(response):
    duration_ms = (time.perf_counter() - g.started_at) * 1000
    tags = [
        f"endpoint:{route_name()}",
        f"method:{request.method}",
        f"status_code:{response.status_code}",
        f"scenario:{g.scenario}",
    ]
    statsd.increment("simulator.requests", tags=tags)
    statsd.distribution("simulator.request.duration", duration_ms, tags=tags)
    if response.status_code >= 500:
        statsd.increment("simulator.errors", tags=tags)

    logger.info(
        "Request completed",
        extra={
            "request_id": g.request_id,
            "scenario": g.scenario,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )
    response.headers["X-Request-ID"] = g.request_id
    return response


@app.errorhandler(SimulatedFailure)
def handle_simulated_failure(error):
    logger.exception(
        "Intentional simulator failure",
        extra={"request_id": g.request_id, "scenario": g.scenario},
    )
    return jsonify({"status": "error", "scenario": g.scenario, "message": str(error)}), 500


@app.route("/health", methods=["GET"])
def health():
    try:
        check_database()
        return jsonify({"status": "ok", "db": "connected"})
    except Exception as error:
        logger.exception("Health check failed", extra={"request_id": g.request_id})
        return jsonify({"status": "error", "db": "disconnected", "error": str(error)}), 500


@app.route("/users", methods=["GET"])
def get_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users ORDER BY id;")
            rows = cur.fetchall()
    return jsonify([{"id": row[0], "name": row[1]} for row in rows])


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
            user_id = cur.fetchone()[0]
    return jsonify({"id": user_id, "name": name}), 201


def run_scenario(scenario):
    g.scenario = scenario
    with tracer.trace("simulator.work", service=DD_SERVICE, resource=scenario) as span:
        span.set_tag("simulation.scenario", scenario)
        span.set_tag("component", "observability-simulator")

        if scenario == "healthy":
            check_database()
            logger.info(
                "Healthy scenario completed",
                extra={"request_id": g.request_id, "scenario": scenario},
            )
            return jsonify({"status": "ok", "scenario": scenario})

        if scenario == "slow":
            delay = random.uniform(SLOW_MIN_SECONDS, SLOW_MAX_SECONDS)
            span.set_metric("simulation.delay_seconds", delay)
            logger.warning(
                "Slow scenario started",
                extra={"request_id": g.request_id, "scenario": scenario},
            )
            time.sleep(delay)
            check_database()
            return jsonify(
                {"status": "ok", "scenario": scenario, "delay_seconds": round(delay, 2)}
            )

        if scenario == "error":
            span.set_tag("error.type", "simulated_failure")
            raise SimulatedFailure("This 500 response is intentional for the Datadog lab")

    return jsonify({"error": f"unknown scenario: {scenario}"}), 400


@app.route("/simulate/<scenario>", methods=["GET"])
def simulate(scenario):
    if scenario == "mixed":
        scenario = random.choices(
            ["healthy", "slow", "error"], weights=[75, 15, 10], k=1
        )[0]
    if scenario not in {"healthy", "slow", "error"}:
        g.scenario = "invalid"
        return jsonify({"error": "scenario must be healthy, slow, error, or mixed"}), 400
    return run_scenario(scenario)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, threaded=True)
