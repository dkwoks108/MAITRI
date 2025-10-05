# 🚀 MAITRI – AI Assistant for Psychological & Physical Well-Being of Astronauts

### 🧠 Problem Statement ID: 25175  
**Theme:** Space Technology | Smart India Hackathon 2025  

---

## 🌍 Overview

**MAITRI** (Multi-modal AI for Therapy, Response & Interaction) is an **AI-powered assistant** that ensures the psychological and physical well-being of astronauts.  
It detects emotions using **facial expressions** and **voice tone**, provides **short supportive conversations**, and reports critical issues — all in an **offline or semi-offline environment**.

---

## 🪐 Objective

Crew members aboard space stations face stress, fatigue, and isolation.  
**MAITRI** helps by:

- Detecting emotional and physical states using **audio-visual input**
- Offering **empathetic, adaptive conversations**
- Supporting astronauts’ **mental resilience** and reducing errors

---

## 🧩 System Architecture

```text
User (Browser)
   ↓
HTML/CSS/JS Frontend  ← Hosted on GitHub Pages
   ↓
   [Captures webcam video & microphone audio]
   ↓
Flask (Python API) running in Google Colab
   ↓
AI Model (Emotion Detection – Facial + Voice Analysis)
   ↓
JSON Response → Frontend displays emotion + adaptive message
