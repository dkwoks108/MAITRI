# MAITRI Usage Examples

## Basic Usage

### Starting the Application

1. **Start Backend Server:**

```bash
# Linux/macOS
./start_backend.sh

# Windows
start_backend.bat

# Manual start
cd backend
python main.py
```

2. **Open Frontend:**

```bash
# Open in default browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows

# Or use Python server
python -m http.server 3000
# Then open http://localhost:3000
```

## API Examples

### Using curl

#### Health Check
```bash
curl http://localhost:8000/
```

Response:
```json
{
  "status": "online",
  "service": "MAITRI AI Assistant",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### Chat with MAITRI
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I feel stressed",
    "emotion_state": "stressed",
    "user_id": "astronaut_1"
  }'
```

Response:
```json
{
  "reply": "I sense you might be feeling stressed. Remember, you're doing amazing work up there. Would you like to try a breathing exercise?",
  "emotion_context": "stressed",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### Save Session Data
```bash
curl -X POST http://localhost:8000/save \
  -H "Content-Type: application/json" \
  -d '{
    "session_data": {
      "emotion": "stressed",
      "confidence": 0.85,
      "alert_triggered": true
    },
    "user_id": "astronaut_1"
  }'
```

Response:
```json
{
  "status": "success",
  "file_id": "data/sessions/session_astronaut_1_20240115_103000.json",
  "message": "Session data saved successfully"
}
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Chat example
def chat_with_maitri(message, emotion="neutral"):
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": message,
            "emotion_state": emotion,
            "user_id": "astronaut_1"
        }
    )
    return response.json()

# Example usage
result = chat_with_maitri("I'm feeling lonely today", "sad")
print(f"MAITRI: {result['reply']}")
```

### Using JavaScript

```javascript
// Chat function
async function chatWithMAITRI(message, emotion = 'neutral') {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      emotion_state: emotion,
      user_id: 'astronaut_1'
    })
  });
  
  const data = await response.json();
  return data.reply;
}

// Example usage
chatWithMAITRI("How should I deal with stress?", "stressed")
  .then(reply => console.log("MAITRI:", reply));
```

## Frontend Examples

### Emotion Detection Flow

```javascript
// 1. Capture video frame
const imageBlob = await captureFrame();

// 2. Record audio segment
const audioBlob = await recordAudioSegment();

// 3. Send to backend
const formData = new FormData();
formData.append('frame', imageBlob, 'frame.jpg');
formData.append('voice', audioBlob, 'voice.webm');

const response = await fetch(API_URL, {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Detected emotion:', result.emotion);
```

### Chat Integration

```javascript
// Send message
async function sendMessage(text) {
  const response = await fetch(CHAT_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: text,
      emotion_state: currentEmotion
    })
  });
  
  const data = await response.json();
  displayBotMessage(data.reply);
}

// Display in chat
function displayBotMessage(message) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'bot-message';
  messageDiv.innerHTML = `<strong>MAITRI:</strong> ${message}`;
  chatContainer.appendChild(messageDiv);
}
```

## Customization Examples

### Adding Custom Emotions

Edit `backend/emotion_analyzer.py`:

```python
def _normalize_emotion(self, emotion: str) -> str:
    emotion_map = {
        'angry': 'stressed',
        'confused': 'uncertain',  # Add new emotion
        # ... other mappings
    }
    return emotion_map.get(emotion.lower(), emotion.lower())
```

### Custom Chatbot Responses

Edit `backend/chatbot.py`:

```python
self.emotion_responses = {
    'stressed': [
        "Custom message for stress...",
        "Another supportive message...",
    ],
    'custom_emotion': [  # Add new emotion responses
        "Response for custom emotion...",
    ]
}
```

### Alert Thresholds

Edit `backend/alert_system.py`:

```python
def __init__(self):
    self.stress_emotions = ['stressed', 'anxious', 'sad']
    self.stress_threshold = 0.75  # Change threshold (0-1)
```

## Data Access Examples

### Reading Session Logs

```python
import json
import os
from glob import glob

# Read all sessions for a user
data_dir = 'backend/data/sessions'
user_id = 'astronaut_1'

sessions = []
for filepath in glob(f'{data_dir}/session_{user_id}_*.json'):
    with open(filepath, 'r') as f:
        session = json.load(f)
        sessions.append(session)

print(f"Found {len(sessions)} sessions")
for session in sessions:
    print(f"- {session['timestamp']}: {session['emotion']}")
```

### Analyzing Alert Reports

```python
import os
from glob import glob

# Read all alerts
alerts_dir = 'backend/data/alerts'

for filepath in glob(f'{alerts_dir}/alert_*.txt'):
    print(f"\n{'='*60}")
    with open(filepath, 'r') as f:
        print(f.read())
```

## Integration Examples

### Webhook Integration

```python
# Add to backend/main.py

@app.post("/webhook")
async def webhook_alert(alert_data: dict):
    """Send alert to external system"""
    import requests
    
    webhook_url = "https://your-webhook-url.com/alert"
    requests.post(webhook_url, json=alert_data)
    
    return {"status": "sent"}
```

### Database Integration

```python
# Add to backend/storage.py

import sqlite3

def save_to_database(session_data):
    conn = sqlite3.connect('maitri.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO sessions (user_id, emotion, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        session_data['user_id'],
        session_data['emotion'],
        session_data['confidence'],
        session_data['timestamp']
    ))
    
    conn.commit()
    conn.close()
```

## Testing Examples

### Unit Test

```python
# test_emotion_detection.py
import pytest
from emotion_analyzer import EmotionAnalyzer

def test_emotion_fusion():
    analyzer = EmotionAnalyzer()
    
    # Test matching emotions
    emotion, conf = analyzer.fuse_emotions(
        'happy', 0.8,
        'happy', 0.7
    )
    
    assert emotion == 'happy'
    assert conf > 0.7
```

### Integration Test

```python
# test_api.py
import requests

BASE_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'online'

def test_chat():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "Hello",
            "emotion_state": "neutral"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert 'reply' in data
```

## Troubleshooting Examples

### Debug Logging

```python
# Add to backend/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Test Emotion Detection

```python
# test_detection.py
from emotion_analyzer import EmotionAnalyzer
from PIL import Image
import io

analyzer = EmotionAnalyzer()

# Test with sample image
image = Image.open('test_image.jpg')
image_bytes = io.BytesIO()
image.save(image_bytes, format='JPEG')
image_bytes = image_bytes.getvalue()

emotion, confidence = analyzer.analyze_video(image_bytes)
print(f"Detected: {emotion} ({confidence:.2%})")
```

## Advanced Examples

### Multi-User Support

```python
# Track multiple astronauts
users = {
    'astronaut_1': {'name': 'Alex', 'emotion_history': []},
    'astronaut_2': {'name': 'Sam', 'emotion_history': []},
}

def track_emotion(user_id, emotion):
    if user_id in users:
        users[user_id]['emotion_history'].append(emotion)
```

### Real-time Monitoring Dashboard

```javascript
// Update dashboard every 5 seconds
setInterval(async () => {
  const response = await fetch('/history/astronaut_1?limit=1');
  const data = await response.json();
  
  if (data.sessions.length > 0) {
    const latest = data.sessions[0];
    updateDashboard(latest);
  }
}, 5000);
```

### Export Reports

```python
# Generate PDF report
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(sessions, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    c.drawString(100, 750, "MAITRI Session Report")
    
    y = 700
    for session in sessions:
        c.drawString(100, y, f"{session['timestamp']}: {session['emotion']}")
        y -= 20
    
    c.save()
```

---

For more examples, see the [GitHub repository](https://github.com/dkwoks108/MAITRI).
