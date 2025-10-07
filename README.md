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
Frontend	HTML5 + Tailwind CSS + Chart.js
Backend	FastAPI (Python)
AI Models	FER, DialoGPT (Transformers)
Storage	Google Drive API (free) + Local fallback
Visualization	Chart.js
Hosting (optional)	Vercel (frontend), Render/Railway (backend)

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Modern web browser with webcam and microphone
- Internet connection (for model downloads)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/dkwoks108/MAITRI.git
cd MAITRI
```

2. **Start the backend:**
```bash
# Linux/macOS
./start_backend.sh

# Windows
start_backend.bat

# Manual start
cd backend
pip install -r requirements.txt
python main.py
```

3. **Open the frontend:**
```bash
# Open index.html in your browser or use Python server
python -m http.server 3000
# Then open http://localhost:3000
```

### First Run
- Backend will download AI models (~500MB) on first run
- Allow camera and microphone permissions in browser
- Click "Start Detection" to begin emotion analysis
- Use chat interface to interact with MAITRI

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup instructions
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide
- **[EXAMPLES.md](EXAMPLES.md)** - Usage examples and code samples
- **[backend/README.md](backend/README.md)** - Backend API documentation

## 🎯 Features Implemented

### ✅ Backend (FastAPI)
- ✅ Emotion detection from video (FER)
- ✅ Audio emotion analysis
- ✅ Emotion fusion algorithm
- ✅ AI chatbot with empathetic responses (DialoGPT)
- ✅ Google Drive integration with local fallback
- ✅ Alert system for stress/fatigue detection
- ✅ RESTful API with CORS support
- ✅ Session logging and data persistence

### ✅ Frontend
- ✅ Space-themed responsive UI
- ✅ Real-time webcam and audio capture
- ✅ Live emotion detection display
- ✅ Interactive chat interface
- ✅ Emotion trend visualization (Chart.js)
- ✅ Alert notifications
- ✅ Session auto-save

### ✅ Storage & Alerts
- ✅ Google Drive API integration
- ✅ Local file storage fallback
- ✅ JSON session logs
- ✅ Alert report generation (JSON + TXT)
- ✅ Session history retrieval

## 📁 Project Structure

```
MAITRI/
├── backend/
│   ├── main.py              # FastAPI server & endpoints
│   ├── emotion_analyzer.py  # Video/audio emotion detection
│   ├── chatbot.py          # AI chatbot with empathetic responses
│   ├── storage.py          # Google Drive integration
│   ├── alert_system.py     # Alert detection & management
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example       # Environment configuration
│   ├── test_backend.py    # Backend tests
│   └── README.md          # Backend documentation
├── index.html             # Main frontend page
├── main.js               # Frontend JavaScript
├── style.css             # Custom styles
├── start_backend.sh      # Linux/macOS startup script
├── start_backend.bat     # Windows startup script
├── README.md             # This file
├── SETUP.md              # Setup instructions
├── DEPLOYMENT.md         # Deployment guide
├── EXAMPLES.md           # Usage examples
└── .gitignore           # Git ignore rules
```

## 🔌 API Endpoints

### GET /
Health check endpoint

### POST /analyze
Analyze emotion from video frame and audio
- **Input**: `frame` (image), `voice` (audio)
- **Output**: Emotion analysis with confidence scores

### POST /chat
Chat with MAITRI AI assistant
- **Input**: `message`, `emotion_state`, `user_id`
- **Output**: AI-generated empathetic response

### POST /save
Save session data to storage
- **Input**: `session_data`, `user_id`
- **Output**: Success confirmation with file ID

### GET /history/{user_id}
Retrieve session history
- **Input**: `user_id`, `limit` (optional)
- **Output**: List of recent sessions

See [backend/README.md](backend/README.md) for detailed API documentation.

## 🎨 UI Preview

The application features:
- **Dark space-themed gradient** background (#0b0d17 → #1b1f3a)
- **Futuristic fonts** (Orbitron, Share Tech Mono)
- **Glowing elements** and smooth animations
- **Responsive design** for desktop and tablet
- **Real-time emotion display** with emojis
- **Interactive chat** with MAITRI AI
- **Live emotion trend chart**

## 🔧 Configuration

### Backend Configuration

Create `backend/.env`:
```bash
HOST=0.0.0.0
PORT=8000
GOOGLE_CREDENTIALS_PATH=credentials.json
USE_GPU=false
LOG_LEVEL=INFO
```

### Google Drive Setup (Optional)

1. Create Google Cloud project
2. Enable Google Drive API
3. Create service account
4. Download credentials as `backend/credentials.json`
5. Share "MAITRI_Data" folder with service account

If not configured, data saves locally to `backend/data/`

## 🧪 Testing

### Test Backend
```bash
cd backend
python test_backend.py
```

### Test API
```bash
# Health check
curl http://localhost:8000/

# Chat test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "emotion_state": "neutral"}'
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

### Quick Deploy Options

**Frontend:**
- Vercel (recommended)
- Netlify
- GitHub Pages

**Backend:**
- Render (recommended)
- Railway
- Google Cloud Run

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **FER** - Facial emotion recognition
- **Transformers** - DialoGPT conversational AI
- **FastAPI** - Modern Python web framework
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Interactive charts

## 📧 Support

- Open an issue on GitHub
- Check [SETUP.md](SETUP.md) for troubleshooting
- Review [EXAMPLES.md](EXAMPLES.md) for usage examples

---

**Built for the future of astronaut well-being monitoring** 🚀✨