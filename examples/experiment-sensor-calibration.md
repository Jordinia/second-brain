---
id: EXP-20260115-103000
type: experiment
title: BME280 Environmental Sensor Calibration & Noise Floor
date: 2026-01-15
status: completed
project: [[project-home-weather-station]]
tags:
  - experiment
  - calibration
  - sensors
parameters:
  sample_rate_hz: 1.0
  duration_minutes: 60
  bus_speed_khz: 100
rag_include: true
---

# Experiment: BME280 Environmental Sensor Calibration & Noise Floor

## 🔬 Objective & Hypothesis
- **Problem Statement**: What is the measurement noise and drift of the BME280 temperature sensor in an enclosed chamber at room temperature?
- **Hypothesis**: Standard deviation of temperature readings over 60 minutes will remain below 0.15°C without forced airflow.

## ⚙️ Experimental Setup
### Environment & Equipment
- **Hardware Platform**: ESP32-WROOM-32 running FreeRTOS.
- **Sensor Breakout**: Bosch BME280 connected via 100 kHz I2C.
- **Reference Standard**: Calibrated laboratory mercury thermometer (21.4°C baseline).

### Test Parameters
```yaml
sampling_interval_ms: 1000
oversampling:
  temperature: "x2"
  pressure: "x4"
  humidity: "x1"
filter_coefficient: 4
```

## 📊 Observations & Results
- **Sample Count**: 3600 samples recorded.
- **Mean Temperature**: 21.32°C.
- **Standard Deviation ($\sigma$)**: 0.08°C.
- **Peak-to-Peak Noise**: 0.24°C.

## 💡 Analysis & Takeaways
The sensor easily satisfied the hypothesis ($\sigma = 0.08^\circ\text{C} < 0.15^\circ\text{C}$). The IIR filter coefficient of 4 effectively dampened rapid fluctuation caused by local ambient draft.

## ⏭️ Next Steps
- [x] Record results in [[project-home-weather-station]]
- [ ] Connect sensor to sleep-cycle firmware and verify startup stabilization time
