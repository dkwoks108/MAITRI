# MAITRI Setup Guide

Complete setup instructions for MAITRI - AI Assistant for Astronauts

## Prerequisites

- Python 3.10 or higher
- Node.js 16+ (optional, for frontend tooling)
- Modern web browser (Chrome, Firefox, Edge)
- Webcam and microphone
- Internet connection (for model downloads)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/dkwoks108/MAITRI.git
cd MAITRI
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Start server
python main.py
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Go back to root directory
cd ..

# Open index.html in browser
# On macOS:
open index.html
# On Linux:
xdg-open index.html
# On Windows:
start index.html

# Or use a simple HTTP server
python -m http.server 3000
# Then open http://localhost:3000
```

## Detailed Setup

### Backend Configuration

#### 1. Install Python Dependencies

The main dependencies are:
- **FastAPI**: Web framework
- **FER**: Facial emotion recognition
- **Transformers**: For DialoGPT chatbot
- **Google API Client**: For Drive storage

```bash
pip install -r backend/requirements.txt
```

First run will download ML models (~500MB):
- DialoGPT-small (~350MB)
- FER models (~150MB)

#### 2. Configure Environment

Edit `backend/.env`:

```bash
# Server settings
HOST=0.0.0.0
PORT=8000

# Google Drive (optional)
GOOGLE_CREDENTIALS_PATH=credentials.json

# Model settings
USE_GPU=false
MODEL_CACHE_DIR=./models

# Logging
LOG_LEVEL=INFO
```

#### 3. Google Drive Setup (Optional)

For cloud storage:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Drive API
4. Create service account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Download JSON key
5. Save as `backend/credentials.json`
6. Create folder in Google Drive named "MAITRI_Data"
7. Share folder with service account email

If not configured, data saves locally to `backend/data/`

### Frontend Configuration

#### 1. Update API URL

Edit `main.js` line 11:

```javascript
const API_URL = "http://localhost:8000/predict";
```

For production, use your deployed backend URL.

#### 2. Browser Permissions

When you first open the app:
1. Allow camera access
2. Allow microphone access

These are required for emotion detection.

## Testing the Setup

### 1. Test Backend

```bash
# In backend directory with venv activated
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Test health endpoint:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "online",
  "service": "MAITRI AI Assistant",
  "version": "1.0.0",
  "timestamp": "2024-..."
}
```

### 2. Test Frontend

1. Open `index.html` in browser
2. Click "Start Detection"
3. Wait for analysis
4. Check that emotion is detected
5. Try sending a chat message

## Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Error: Port 8000 already in use**
```bash
# Change port in .env or run on different port
uvicorn main:app --port 8001
```

**Error: Models not downloading**
- Check internet connection
- Ensure sufficient disk space (~1GB)
- Try manually downloading models:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
```

**Error: Google Drive authentication failed**
- Verify `credentials.json` exists
- Check service account has correct permissions
- Ensure Drive API is enabled

### Frontend Issues

**Error: Cannot connect to backend**
- Verify backend is running on port 8000
- Check API_URL in `main.js`
- Check browser console for CORS errors

**Error: Camera not working**
- Allow camera permissions in browser
- Check camera is not used by another application
- Try different browser

**Error: Microphone not working**
- Allow microphone permissions in browser
- Check microphone is selected as default device
- Verify microphone is not muted

**Error: Emotion not detected**
- Ensure good lighting for face detection
- Position face clearly in camera view
- Check backend logs for errors

## Development Tips

### Running in Development Mode

Backend with auto-reload:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend with live server:
```bash
# Using Python
python -m http.server 3000

# Using Node.js
npx http-server -p 3000
```

### Checking Logs

Backend logs:
```bash
# In backend directory
tail -f logs/maitri.log
```

Browser logs:
- Open Developer Tools (F12)
- Check Console tab

### Testing Endpoints

Use curl or Postman:

```bash
# Health check
curl http://localhost:8000/

# Analyze (requires files)
curl -X POST http://localhost:8000/analyze \
  -F "frame=@test_frame.jpg" \
  -F "voice=@test_audio.webm"

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "emotion_state": "neutral"}'
```

## Project Structure

```
MAITRI/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── emotion_analyzer.py  # Emotion detection
│   ├── chatbot.py          # AI chatbot
│   ├── storage.py          # Google Drive integration
│   ├── alert_system.py     # Alert management
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example       # Environment template
│   └── README.md          # Backend documentation
├── index.html             # Main frontend page
├── main.js               # Frontend JavaScript
├── style.css             # Custom styles
├── README.md             # Project overview
├── SETUP.md              # This file
├── DEPLOYMENT.md         # Deployment guide
└── .gitignore           # Git ignore rules
```

## Next Steps

1. **Customize Responses**: Edit `backend/chatbot.py` to add personalized responses
2. **Improve Models**: Fine-tune models with astronaut-specific data
3. **Add Features**: Implement additional health monitoring
4. **Deploy**: Follow `DEPLOYMENT.md` to deploy to production
5. **Monitor**: Set up logging and monitoring

## Getting Help

- Check [README.md](README.md) for project overview
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment
- Check backend logs for errors
- Open GitHub issue for bugs
- Contact support for questions

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - see LICENSE file for details

---

Last updated: 2024
