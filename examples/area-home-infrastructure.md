---
id: AREA-20260101-120000
type: area
title: Home & Hardware Infrastructure
status: active
review_cadence: monthly
tags:
  - area
  - infrastructure
  - home
rag_include: true
---

# Home & Hardware Infrastructure

## 🌐 Domain Overview
Continuous maintenance, telemetry monitoring, and lifecycle management for local home automation, workstations, and network equipment.

## 🎯 Standards & Commitments
- Keep 100% of telemetry metrics backed up offsite weekly.
- Maintain thermal limits below 65°C across all home compute nodes.
- Document all circuit wiring and GPIO pin mappings in project charters.

## 🚀 Active Projects
- [[project-home-weather-station|Home Weather Station & Telemetry Monitor]]

## 📚 Evergreen Knowledge & Resources
- [[decision-use-postgresql|ADR: Adopt PostgreSQL with TimescaleDB]]
- [[experiment-sensor-calibration|EXP: BME280 Sensor Calibration]]

## 🔄 Periodic Review Checklist
- [ ] Inspect solar battery health and outdoor enclosures
- [ ] Verify database WAL archives and disk space
- [ ] Update firmware packages across microcontrollers
