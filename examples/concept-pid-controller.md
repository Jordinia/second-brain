---
id: KB-20260108-161500
type: concept
title: Proportional-Integral-Derivative (PID) Controller
status: evergreen
tags:
  - concept
  - controls
  - algorithms
aliases:
  - PID Control
  - Three-Term Controller
confidence: verified
sources: []
rag_include: true
---

# Proportional-Integral-Derivative (PID) Controller

## 📌 Definition & Mental Model
A PID controller is a generic feedback loop mechanism that continuously computes an error value $e(t)$ as the difference between a desired setpoint $r(t)$ and a measured process variable $y(t)$, applying a correction based on proportional, integral, and derivative terms.

```text
       r(t)    +   e(t)   ┌──────────────┐   u(t)   ┌─────────┐
Setpoint ─────>○─────────>│ Controller   ├─────────>│ Process ├───┬──> y(t)
               ^-         └──────────────┘          └─────────┘   │
               │                                                  │
               └──────────────────────────────────────────────────┘
```

---

## ⚙️ Mathematical Formulation & Mechanics

The continuous control law is given by:

$$u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

Where:
- **$K_p$ (Proportional)**: Generates an output proportional to the current error. High $K_p$ increases responsiveness but risks overshoot and oscillation.
- **$K_i$ (Integral)**: Accumulates past errors over time, eliminating steady-state offset error. Risks integral windup if output saturates.
- **$K_d$ (Derivative)**: Anticipates future error based on current rate of change, providing damping against overshoot. Highly sensitive to measurement noise.

---

## 🛠️ Practical Implementation (Discrete Anti-Windup Form)

```python
class DiscretePID:
    def __init__(self, kp: float, ki: float, kd: float, dt: float, min_out: float, max_out: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.min_out = min_out
        self.max_out = max_out
        
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, setpoint: float, measured: float) -> float:
        error = setpoint - measured
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with clamping anti-windup
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        
        # Derivative term on measurement to avoid derivative kick
        d_term = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error
        
        # Compute raw output and clamp
        output = p_term + i_term + d_term
        clamped_output = max(self.min_out, min(output, self.max_out))
        
        # Prevent integral accumulation if saturated
        if output != clamped_output:
            self.integral -= error * self.dt
            
        return clamped_output
```

---

## ⚠️ Trade-offs & Pitfalls
- **Integral Windup**: When actuators saturate (e.g., motor reaching full voltage), the integral continues accumulating error, causing sluggish recovery. Always implement clamping or back-calculation anti-windup.
- **Derivative Kick**: Step changes in setpoint cause instantaneous spikes in $\frac{de(t)}{dt}$. Calculate derivative directly on the feedback measurement $\frac{dy(t)}{dt}$ rather than error.
- **High-Frequency Sensor Noise**: Differentiating raw sensor noise produces erratic control effort. Use a low-pass filter on the derivative term.

---

## 🔗 Related Notes
- [[experiment-sensor-calibration|Sensor Noise Mitigation in Experiments]]
- [[project-home-weather-station|Telemetry Hardware Integration]]
