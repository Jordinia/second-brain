---
id: LIT-20260112-142000
type: literature
title: "Visual SLAM and Spatial AI: A Decade in Review"
authors:
  - "Elena Rostova"
  - "Marcus Vance"
year: 2025
venue: "Journal of Field Robotics"
doi: "10.1002/rob.99999"
url: "https://example.org/papers/visual-slam-review"
reading_status: read
tags:
  - literature
  - slam
  - robotics
  - computer-vision
rag_include: true
---

# Visual SLAM and Spatial AI: A Decade in Review

## 📌 One-Line Executive Summary
A comprehensive survey comparing feature-based, direct, and neural implicit representations for real-time robotic localization and dense 3D mapping.

## 💡 Key Contributions
- Chronological taxonomy contrasting classic sparse bundle adjustment (ORB-SLAM3) against dense radiance-field methods (Gaussian Splatting SLAM).
- Empirical benchmark across EuRoC and TUM-VI datasets comparing trajectory drift ($ATE$) and compute requirements (FPS / Watts).
- Systematic breakdown of degenerate visual environments: low-texture corridors, motion blur, and dynamic obstacles.

## 🔬 Methodology & Architecture
- **Front-End Tracking**: Comparison of optical flow, learned feature descriptors (SuperPoint), and direct photometric error minimization.
- **Back-End Optimization**: Factor graphs solved via Levenberg-Marquardt within keyframe sliding windows.
- **Loop Closure**: DBoW2 bag-of-words vs deep metric embedding retrieval.

## 📊 Evaluation & Benchmarks
- Classical keyframe methods still dominate on resource-constrained embedded companion computers (<15W TDP).
- Neural implicit methods produce photorealistic novel view synthesis but exhibit 4–6x latency penalties on embedded hardware.

## ⚠️ Limitations & Open Challenges
- Fast aggressive angular maneuvers lead to catastrophic tracking loss under rolling-shutter camera sensors.
- Purely geometric SLAM lacks semantic reasoning for dynamic object exclusion.

## 🎯 Practical Synthesis & Relevance
- For embedded robotic projects requiring deterministic real-time tracking, sparse feature-based graph SLAM remains the optimal baseline.
- Informing future controller design in [[concept-pid-controller]].

## 🔗 Key Citations & Connections
- [[concept-pid-controller|PID Controller Theory]]
- [[project-home-weather-station|Telemetry Hardware Platforms]]
