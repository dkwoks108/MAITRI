# Build Working Prototype for “MAITRI – AI Assistant for Astronauts”

🎯 Objective

Build a responsive, space-themed AI assistant web app (named MAITRI) that detects astronauts’ emotional and physical well-being using audio + video input, provides empathetic conversation, and stores session data to Google Drive.

🌐 System Overview
Layer	Purpose	Tech / Model
Frontend (UI)	Collect audio + video from astronaut, display chatbot, show emotional state	Next.js / React + Tailwind CSS (space theme)
Backend API	Receive data, run AI models, generate responses, log results	FastAPI (Python)
AI Models	Analyze audio + video emotions + chat	SpeechBrain, FER + MediaPipe, DialoGPT
Storage	Store logs, states, conversation summaries	Google Drive API (free tier)
Alert Logic	Detect high stress / fatigue → save alert report	Python rule engine
Visualization	Emotion trend chart / alert display	Chart.js or Plotly (frontend)

🧩 User Flow Diagram (Data Flow + Interaction)
┌───────────────────────────────────────────────────┐
│                  Astronaut (User)                 │
│   - Talks & looks at webcam                       │
│   - Interacts with MAITRI chat UI                 │
└───────────────┬───────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│      1️⃣ Responsive Space-Themed UI (Next.js)     │
│  - Captures mic & webcam input                    │
│  - Shows live emotional state (icon/graph)        │
│  - Displays chat messages from MAITRI             │
└───────────────┬───────────────────────────────────┘
                │  (Audio/Video sent via API)
                ▼
┌───────────────────────────────────────────────────┐
│       2️⃣ FastAPI Backend (Python Server)          │
│  - Accepts input frames/chunks                    │
│  - Passes to ML models                            │
│      • SpeechBrain → audio emotion                │
│      • FER + MediaPipe → face & emotion           │
│  - Fuses outputs → final state                    │
└───────────────┬───────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│         3️⃣ MAITRI AI Assistant Logic              │
│  - Uses emotional state to choose empathetic reply │
│  - DialoGPT (Hugging Face) → chat message          │
│  - If stress/fatigue high → trigger alert logic    │
└───────────────┬───────────────────────────────────┘
                │
     ┌──────────┴───────────┐
     ▼                      ▼
┌────────────────────┐  ┌──────────────────────────┐
│ 4️⃣ Chat Response   │  │ 5️⃣ Alert & Storage Layer │
│ (Back to UI via WS)│  │ - Save logs & state JSON │
│                    │  │ - Upload to Google Drive │
└──────────┬─────────┘  │   using Google Drive API │
           │             └──────────┬──────────────┘
           ▼                        ▼
    ┌────────────────────┐   ┌──────────────────────┐
    │Astronaut Dashboard │   │Ground Team Access    │
    │  (Trend / Mood)    │   │  (Alert Reports)     │
    └────────────────────┘   └──────────────────────┘

⚙️ Implementation Details
🖥️ Frontend (Next.js)

Use Tailwind CSS + space theme (dark mode, stars, gradients).

Components:

Webcam Recorder (MediaPipe compatible)

Microphone Recorder (WebAudio API)

Chat Interface (messages + bot replies)

Emotion Status Indicator (emoji/graph)

Responsive for desktop + tablet.

🧠 Backend (FastAPI)

Endpoints:

POST /analyze
# Receives audio + video base64, returns emotion result.

POST /chat
# Takes emotion state + message, returns chatbot reply.

POST /save
# Stores session logs to Google Drive.

🧩 AI Models (Free)
Task	Model	Library
Audio Emotion	SpeechBrain	PyTorch
Video Emotion	FER	Keras
Face/Body Detection	MediaPipe	Google
Chatbot	DialoGPT (Hugging Face)	Transformers
Fusion	Custom weighted rule	Python logic
☁️ Database / Storage

Use Google Drive API as your data store:

Save logs as JSON or CSV files (each session = 1 file).

Folder structure:
/MAITRI_Data/
    /sessions/
        session_2025-10-07_1.json
    /alerts/
        alert_2025-10-07_critical.txt

Authentication: use OAuth2 credentials for Google Drive API (free).

🧾 Example File Stored on Drive
{
  "astronaut": "User_1",
  "timestamp": "2025-10-07T12:30:00Z",
  "audio_emotion": "stressed",
  "video_emotion": "tired",
  "final_emotion": "fatigued",
  "chat_summary": "MAITRI suggested a breathing exercise.",
  "alert_triggered": true
}

🎨 UI Theme Inspiration

Background: dark space gradient (#0b0d17 → #1b1f3a)

Floating glowing icons (planets, AI orb)

Font: futuristic (Orbitron or Exo 2)

Animation: floating particles (like stars)

MAITRI Avatar: glowing AI sphere or astronaut icon

🚀 Prototype Flow Summary

1️⃣ Astronaut opens app → MAITRI greets.
2️⃣ Camera & mic on → data captured every few seconds.
3️⃣ Backend processes → detects emotion & fatigue.
4️⃣ MAITRI responds → supportive, adaptive conversation.
5️⃣ Logs saved to Google Drive → available to review.
6️⃣ Alerts triggered → if stress/fatigue too high.

🧰 Tech Stack Summary
Layer	Tool
Frontend	Next.js + Tailwind CSS + MediaPipe
Backend	FastAPI (Python)
AI Models	SpeechBrain, FER, DialoGPT
Storage	Google Drive API (free)
Visualization	Chart.js / Plotly
Hosting (optional)	Vercel (frontend), Render/Google Colab (backend)