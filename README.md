# 📊 Observability POC (Prometheus + Loki + Grafana + OpenTelemetry)

This project demonstrates a **complete observability stack** using:

* **OpenTelemetry Collector** → Collects telemetry data
* **Prometheus** → Stores metrics
* **Loki** → Stores logs
* **Grafana** → Visualization dashboard
* **k6** → Generates load (simulated traffic)

---

# 🧠 Architecture Overview

```
k6 (load generator)
        ↓
OpenTelemetry Collector
        ↓
   ┌───────────────┬───────────────┐
   ↓               ↓               ↓
Prometheus      Loki           Debug Logs
(metrics)       (logs)
        ↓
     Grafana (UI)
```

---

# 📁 Project Structure

```
monitoring-observability/
├── README.md                 # Documentation and setup guide
├── docker-compose.yaml        # Container orchestration
├── loki-config.yaml         # Loki log aggregation config
├── otel-config.yaml         # OpenTelemetry collector config
├── prometheus.yaml          # Prometheus metrics scraping config
├── scripts/                # Utility and test scripts
│   └── load-test.js       # k6 load testing script
├── send_log.py            # Manual log injection script
├── logs.json             # Sample log data format
├── provisioning/          # Grafana auto-provisioning
│   └── datasources/
│       └── datasources.yaml
├── grafana-data/         # Grafana persistent data
│   ├── grafana.db       # Grafana SQLite database
│   └── plugins/         # Installed Grafana plugins
│       ├── grafana-exploretraces-app/
│       ├── grafana-lokiexplore-app/
│       ├── grafana-metricsdrilldown-app/
│       └── grafana-pyroscope-app/
└── loki-data/            # Loki log storage
    ├── chunks/           # Compressed log data blocks
    ├── tsdb-shipper-active/  # Active time-series data
    └── wal/              # Write-ahead log for durability
```

---

# ⚙️ Prerequisites

* Docker
* Docker Compose
* Open ports:

  * 3000 → Grafana
  * 9090 → Prometheus
  * 3100 → Loki

---

# 🚀 Setup & Execution Steps

## 1️⃣ Clone / Navigate to Project

```bash
cd ~/monitoring-observability
```

---

## 2️⃣ Start the Stack

```bash
docker-compose down -v
docker-compose pull
docker-compose up -d
```

---

## 3️⃣ Verify Containers

```bash
docker ps
```

Expected:

* grafana → Up
* prometheus → Up
* loki → Up
* otel-collector → Up
* sample-app (k6) → Running

---

## 4️⃣ Check Logs (if any issue)

```bash
docker logs monitoring-observability_loki_1
docker logs monitoring-observability_otel-collector_1
```

---

# 🌐 Access Services

| Service    | URL                  |
| ---------- | -------------------- |
| Grafana    | http://<EC2-IP>:3000 |
| Prometheus | http://<EC2-IP>:9090 |
| Loki API   | http://<EC2-IP>:3100 |

---

# 🔐 Grafana Login

```
Username: admin
Password: admin
```

---

# 📊 Configure Grafana

## Add Prometheus

1. Go to → Settings → Data Sources
2. Add → Prometheus
3. URL:

```
http://prometheus:9090
```

---

## Add Loki

**Note:** Loki is automatically configured via provisioning!

1. Go to → Settings → Data Sources
2. Loki should already be listed as default
3. URL: `http://loki:3100` (auto-configured)

If manual setup needed:
```
http://loki:3100
```

---

# 🧪 Load Testing (k6)

The system automatically runs:

```
scripts/load-test.js
```

It:

* Simulates 5 users
* Runs for 10 minutes
* Sends traffic to OpenTelemetry (http://otel-collector:4318/v1/traces)

# 🧪 Manual Log Testing

For testing log injection manually:

```bash
python3 send_log.py
```

This sends a sample log to OpenTelemetry Collector using the format in `logs.json`.

---

# ⚠️ Important Notes

### 1. Logs vs Traces

Current setup generates:

* ✔ Metrics (via OpenTelemetry → Prometheus)
* ✔ Traces (via k6 load test)
* ✔ Logs (via send_log.py or manual injection)
* ❌ Real application logs (requires SDK integration)

---

### 2. Loki Integration

* Uses OTLP HTTP endpoint
* Requires Loki 3.x
* Structured metadata enabled

---

### 3. Common Issues

#### ❌ Loki crash

* Cause: invalid config or wrong version
* Fix: use `grafana/loki:3.0.0`

---

#### ❌ OTEL Collector exit

* Cause: unsupported exporter
* Fix: use `otlphttp` exporter

---

#### ❌ No logs in Grafana

* Cause: no real logs generated
* Fix: add application logging or OTEL SDK

---

# 🧠 Learning Outcomes

This project helps understand:

* Observability architecture
* Metrics vs Logs vs Traces
* OpenTelemetry pipelines
* Real-world debugging of distributed systems

---

# 🔮 Next Improvements

* Add **Tempo** for distributed tracing
* Add real application (Node.js / Java) with OTEL SDK
* Create custom Grafana dashboards for metrics/logs
* Add alerting rules (Prometheus/Loki)
* Add log retention policies
* Integrate with MongoDB backup monitoring

---

# 🏁 Stop the Stack

```bash
docker-compose down
```

---

# 💡 Pro Tip

This setup is **interview-level ready** for:

* DevOps Engineer
* SRE roles
* Platform Engineering discussions

---

# 👨‍💻 Author

Observability POC built for hands-on DevOps learning and real-world debugging.

