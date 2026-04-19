# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AuroraIOT is a real-time energy monitoring backend that ingests PZEM-004t sensor data from ESP32 microcontrollers via MQTT and exposes it through a REST API. The stack is Django 5 + Django REST Framework + TimescaleDB (PostgreSQL with time-series extension) + Paho MQTT.

## Commands

**Development server:**
```bash
python manage.py runserver
# Default settings: AuroraIOT.settings.dev (MQTT enabled)
# To run without MQTT:
DJANGO_SETTINGS_MODULE=AuroraIOT.settings.dev_mqtt_off python manage.py runserver
```

**Database setup (full reset):**
```bash
./rebuilddatabasePostgre.sh
# Seeds initial data from queriespostgre.sql
```

**Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Disable MQTT at runtime:**
```bash
python manage.py mqttoff
```

**Docker (production):**
```bash
docker compose up -d
# Services: nginx (80/443), auroraiot (9000), auroraiotdb (5432), mosquitto (1883)
```

**Tests:** No test suite is configured. `tests.py` files exist but are empty.

**Linting:** No linter is configured.

## Settings Architecture

Settings live in `AuroraIOT/settings/` and follow an inheritance pattern:

| File | Use |
|---|---|
| `common.py` | Shared base |
| `dev.py` | Local dev (DEBUG=True, CORS open, MQTT on) |
| `dev_mqtt_off.py` | Dev without MQTT |
| `prod.py` | Production (DEBUG=False, restricted hosts, MQTT on) |
| `prod_mqtt_off.py` | Production without MQTT |

`manage.py` defaults to `AuroraIOT.settings.dev`. Gunicorn (`gunicorn.conf.py`) uses `prod`.

Secrets and broker credentials are loaded from `.env` via `python-decouple`. Keys include `SECRET_KEY`, `DEV_MQTT_SERVER/PORT/USER/PASSWORD`, `PROD_MQTT_SERVER/PORT/USER/PASSWORD`, and separate DB credentials for dev/prod.

## App Architecture

### `sensors/`
Core domain app. Three regular models plus one time-series model:

- `Sensor_Type` — lookup table for sensor categories
- `Sensor_Configuration` — optional JSON config with `update_ms` and `params`
- `Sensor` — the physical device; FK to `Sensor_Type` and optionally `Sensor_Configuration`
- `Data_PZEM004t` — extends `TimescaleModel` (abstract base from `django-timescaledb`); stores energy readings (volts, amps, watts, energy kWh, frequency, power_factor) with a `time` field partitioned by 1-day intervals

`TimescaleModel` provides `TimescaleDateTimeField` on `time` and a `TimescaleManager`. Queries against `Data_PZEM004t` benefit from TimescaleDB hypertable optimizations automatically.

### `mqttclient/`
Handles real-time ingestion:

- `Data_Received` — raw JSON payload storage (FK to `Sensor`)
- `apps.py` — starts the MQTT client thread in `ready()` (skipped when `MQTT_ACTIVE=False`)
- `mqttclient.py` — Paho MQTT client; subscribes to `auroraiot/energy`, parses incoming JSON, writes to `Data_Received` and `Data_PZEM004t`; reconnects with exponential backoff (max 12 retries)

MQTT payload format on topic `auroraiot/energy`:
```json
{"sensor_id": 1, "data": {"address": 1, "voltage": 220, "current": 5.25, "frequency": 60, "power": 1155.0, "energy": 1.25, "pf": 0.95}}
```

## REST API

Base path: `/api/`  
DRF default permission: `IsAuthenticatedOrReadOnly`  
Pagination: page number, 10 per page  
Filtering: `django-filter` + DjangoFilterBackend

**Nested routing** via `drf-nested-routers`:

| Endpoint | ViewSet | Notes |
|---|---|---|
| `GET /api/sensors/` | `SensorViewSet` (ReadOnly) | filter: `id`; search: `name`, `brand` |
| `GET /api/sensors/{sensor_pk}/data/` | `SensorDataViewSet` (ReadOnly) | filter: `time__gt`, `time__lt`; order: `-time` |
| `GET /api/docs/` | — | CoreAPI auto-schema |

`SensorDataViewSet` uses `sensor_pk` from the URL to filter `Data_PZEM004t`; the queryset is built in `get_queryset()`.

## Dependency Management

The project uses both `Pipfile` (pipenv) and `pyproject.toml`. Docker builds with `pipenv install --system`. For local dev, use either `pipenv install` or `pip install -r requirements.txt`.

Python version: **3.10** (`.python-version`).

## Docker / Production

`docker-compose.yaml` defines four services on `auroraiot_net` bridge:
- **nginx** — reverse proxy
- **mosquitto** — MQTT broker; internal hostname `mosquitto`
- **auroraiot** — Gunicorn on port 9000 (1 worker configured; increase for production load)
- **auroraiotdb** — TimescaleDB (Postgres 16), volume `db-data`

The Dockerfile runs migrations (with `prod_mqtt_off` settings) and `collectstatic` at build time.

Logs are written to `logs/django-general.log`, `logs/gunicorn-access.log`, and `logs/gunicorn-error.log`.
