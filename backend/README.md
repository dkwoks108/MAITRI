# MAITRI Backend API

FastAPI backend for MAITRI - AI Assistant for Astronauts

## Features

- **Emotion Analysis**: Video and audio emotion detection using FER and audio analysis
- **AI Chatbot**: Empathetic conversational AI using DialoGPT
- **Google Drive Storage**: Session data and alert storage
- **Alert System**: Automatic stress/fatigue detection
- **RESTful API**: Clean endpoints for frontend integration

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

### 3. Google Drive Setup (Optional)

For Google Drive integration:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Drive API
4. Create service account credentials
5. Download `credentials.json` to backend directory
6. Share your Google Drive folder with the service account email

If credentials are not provided, the system will use local file storage as fallback.

### 4. Run Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### GET /
Health check endpoint

### POST /analyze
Analyze emotion from video frame and audio
- **Input**: `frame` (image file), `voice` (audio file)
- **Output**: Emotion analysis with confidence scores

### POST /chat
Chat with MAITRI AI assistant
- **Input**: `message`, `emotion_state`, `user_id`
- **Output**: AI-generated empathetic response

### POST /save
Save session data to storage
- **Input**: `session_data` (dict), `user_id`
- **Output**: Success confirmation with file ID

### GET /history/{user_id}
Retrieve session history
- **Input**: `user_id`, `limit` (optional)
- **Output**: List of recent sessions

### POST /predict (Legacy)
Backward compatible endpoint for existing frontend

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── emotion_analyzer.py  # Video/audio emotion detection
├── chatbot.py          # Conversational AI
├── storage.py          # Google Drive integration
├── alert_system.py     # Alert detection and management
├── requirements.txt    # Python dependencies
├── .env.example       # Environment configuration template
└── README.md          # This file
```

## Models Used

- **FER**: Facial Emotion Recognition for video analysis
- **DialoGPT**: Microsoft's conversational AI model
- **Audio Analysis**: Custom audio emotion detection (can be extended with SpeechBrain)

## Storage

### Local Fallback
If Google Drive is not configured, data is stored locally:
- `data/sessions/` - Session logs
- `data/alerts/` - Alert reports

### Google Drive
When configured, data is stored in:
- `MAITRI_Data/sessions/` - Session logs
- `MAITRI_Data/alerts/` - Alert reports

## Development

### Adding New Endpoints

Add new endpoints in `main.py`:

```python
@app.post("/new-endpoint")
async def new_endpoint(request: RequestModel):
    # Your logic here
    return {"result": "success"}
```

### Extending Emotion Analysis

Modify `emotion_analyzer.py` to add new emotion detection methods or improve fusion logic.

### Customizing Chatbot

Edit `chatbot.py` to add new response templates or fine-tune the conversational model.

## Troubleshooting

### Port Already in Use
Change the port in `.env` or run with different port:
```bash
uvicorn main:app --port 8001
```

### Model Download Issues
Models will download on first run. Ensure you have:
- Stable internet connection
- Sufficient disk space (~500MB for models)

### Google Drive Authentication
- Verify `credentials.json` is in the backend directory
- Check service account has Drive API access
- Ensure folder is shared with service account email

## License

MIT License - See LICENSE file for details
