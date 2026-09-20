---
id: PRJ-20260110-090000
type: project
title: Home Weather Station & Telemetry Monitor
status: active
start_date: 2026-01-10
target_date: 2026-03-31
completed_date: 
area: [[area-home-infrastructure]]
tags:
  - project
  - hardware
  - iot
rag_include: true
---

# Home Weather Station & Telemetry Monitor

## 🎯 Project Charter
### Objective
Deploy a solar-powered environmental telemetry station that monitors ambient temperature, relative humidity, and barometric pressure, publishing 1-minute metrics over MQTT to a local database.

### Scope & Boundaries
- **In Scope**: ESP32 microcontroller firmware, BME280 sensor breakout, solar battery management, and MQTT telemetry broker ingestion.
- **Out of Scope**: Long-range LoRa transmission (deferred to v2) or cloud SaaS dashboard subscriptions.

## 🗺️ Milestones & Roadmap
- [x] **M1: Sensor Bench Verification**: Verify BME280 readings over I2C in [[experiment-sensor-calibration]]. (Target: 2026-01-20)
- [ ] **M2: Solar Power Harness**: Bench test LiPo charging circuit under daylight simulation. (Target: 2026-02-15)
- [ ] **M3: Enclosure & Outdoor Deployment**: 3D print Stevenson screen and mount outdoors. (Target: 2026-03-15)

## 📋 Task Breakdown
- [x] Wire BME280 to ESP32 DevKit over I2C (SDA: GPIO21, SCL: GPIO22)
- [x] Validate sensor noise and baseline accuracy in [[experiment-sensor-calibration]]
- [ ] Configure database ingestion schema using [[decision-use-postgresql]]
- [ ] Implement deep sleep mode (10s active, 50s deep sleep) to minimize power draw

## 🔗 Related Notes & Resources
- **Architecture Decision**: [[decision-use-postgresql|ADR: Adopt PostgreSQL for Sensor Telemetry]]
- **Calibration Experiment**: [[experiment-sensor-calibration|EXP: BME280 Thermal Response Calibration]]
- **Control Theory**: [[concept-pid-controller|PID Controller Theory]]

## 📝 Activity & Log
- **2026-01-10**: Project kicked off; BOM parts ordered.
- **2026-01-15**: Sensor arrived and verified on bench.
