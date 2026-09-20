---
id: ADR-20260111-150000
type: decision
title: Adopt PostgreSQL with TimescaleDB for Sensor Telemetry Storage
status: accepted
date: 2026-01-11
deciders:
  - "System Architect"
tags:
  - decision
  - adr
  - database
  - architecture
rag_include: true
---

# ADR: Adopt PostgreSQL with TimescaleDB for Sensor Telemetry Storage

## 📋 Context & Problem Statement
The [[project-home-weather-station]] requires a persistent time-series telemetry store for 1-minute environmental sensor logs. The storage engine must run on low-power local hardware (Raspberry Pi 4 / mini PC), support SQL querying for analytical aggregations, and integrate cleanly with standard visualization tools (Grafana).

---

## ⚖️ Decision Drivers
1. **Low Memory Footprint**: Must operate comfortably within 1GB RAM constraints.
2. **Standard SQL Interface**: Prefer relational SQL over proprietary time-series query languages.
3. **Data Retention Management**: Easy automated rollups and retention policies (drop data older than 90 days).
4. **Tooling Ecosystem**: Direct integration with Python scripts, SQLAlchemy, and Grafana.

---

## 🎯 Considered Options
1. **Option A: PostgreSQL with TimescaleDB Extension**
2. **Option B: InfluxDB v2 (Flux)**
3. **Option C: SQLite with Custom Partitioning**

---

## 🏆 Decision Outcome
**Chosen Option**: **Option A: PostgreSQL with TimescaleDB** because it offers standard ANSI SQL, automatic chunk-based partitioning, built-in continuous aggregates, and rock-solid ACID reliability without introducing a specialized query DSL.

### Positive Consequences
- Can combine time-series telemetry tables with regular relational metadata (device tables, sensor calibrations) in the same database.
- Standard PostgreSQL drivers are universally available across Python, Node, and C++.
- Continuous aggregates automatically calculate hourly and daily averages in the background.

### Negative Consequences / Accepted Risks
- Higher write overhead than raw InfluxDB under extreme ingest rates (>100,000 writes/sec), though our station produces <10 writes/sec.
- Requires regular backup maintenance using `pg_dump` or WAL archiving.

---

## 📊 Pros and Cons of the Options

### Option A: PostgreSQL with TimescaleDB
- **Pros**: Full SQL compliance, relational joins, hypertable chunking, outstanding Grafana support.
- **Cons**: Slightly higher memory usage than SQLite.

### Option B: InfluxDB v2
- **Pros**: High compression ratio, optimized purely for time-series.
- **Cons**: Steep learning curve for Flux scripting; weaker join support against relational metadata.

### Option C: SQLite
- **Pros**: Zero daemon configuration, single-file deployment.
- **Cons**: Concurrent write locking under continuous ingest; lacks native time-series downsampling.

---

## 🔗 Links & Related Records
- [[project-home-weather-station|Telemetry Project Charter]]
- [[experiment-sensor-calibration|Sensor Noise Measurements]]
