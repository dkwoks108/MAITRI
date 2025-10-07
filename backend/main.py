"""
MAITRI Backend API Server
FastAPI server for emotion detection, chatbot interaction, and data storage
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
import logging
from datetime import datetime
import json
import io

# Import modules
from emotion_analyzer import EmotionAnalyzer
from chatbot import MAITRIChatbot
from storage import GoogleDriveStorage
from alert_system import AlertSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MAITRI API",
    description="AI Assistant for Astronaut Emotional Well-being",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
emotion_analyzer = EmotionAnalyzer()
chatbot = MAITRIChatbot()
storage = GoogleDriveStorage()
alert_system = AlertSystem()

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    emotion_state: str
    user_id: Optional[str] = "astronaut_1"

class ChatResponse(BaseModel):
    reply: str
    emotion_context: str
    timestamp: str

class SaveRequest(BaseModel):
    session_data: Dict
    user_id: Optional[str] = "astronaut_1"

class AnalyzeResponse(BaseModel):
    emotion: str
    confidence: float
    video_emotion: str
    audio_emotion: str
    message: str
    timestamp: str
    alert_triggered: bool


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "MAITRI AI Assistant",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_emotion(
    frame: UploadFile = File(...),
    voice: UploadFile = File(...)
):
    """
    Analyze emotion from video frame and audio
    
    Args:
        frame: Image file from webcam
        voice: Audio file from microphone
    
    Returns:
        Emotion analysis results with confidence scores
    """
    try:
        logger.info("Received analyze request")
        
        # Read files
        image_bytes = await frame.read()
        audio_bytes = await voice.read()
        
        # Analyze video emotion
        video_emotion, video_confidence = emotion_analyzer.analyze_video(image_bytes)
        logger.info(f"Video emotion: {video_emotion} ({video_confidence:.2f})")
        
        # Analyze audio emotion
        audio_emotion, audio_confidence = emotion_analyzer.analyze_audio(audio_bytes)
        logger.info(f"Audio emotion: {audio_emotion} ({audio_confidence:.2f})")
        
        # Fuse emotions
        final_emotion, final_confidence = emotion_analyzer.fuse_emotions(
            video_emotion, video_confidence,
            audio_emotion, audio_confidence
        )
        
        # Check for alerts
        alert_triggered = alert_system.check_alert(final_emotion, final_confidence)
        
        # Generate empathetic message
        message = chatbot.generate_emotion_response(final_emotion)
        
        response = AnalyzeResponse(
            emotion=final_emotion,
            confidence=final_confidence,
            video_emotion=video_emotion,
            audio_emotion=audio_emotion,
            message=message,
            timestamp=datetime.now().isoformat(),
            alert_triggered=alert_triggered
        )
        
        logger.info(f"Analysis complete: {final_emotion}")
        return response
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with MAITRI AI assistant
    
    Args:
        request: Chat request with message and emotion state
    
    Returns:
        AI-generated empathetic response
    """
    try:
        logger.info(f"Chat request from {request.user_id}: {request.message}")
        
        # Generate response using chatbot
        reply = chatbot.generate_response(
            message=request.message,
            emotion_state=request.emotion_state
        )
        
        response = ChatResponse(
            reply=reply,
            emotion_context=request.emotion_state,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Chat response generated: {reply[:50]}...")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.post("/save")
async def save_session(request: SaveRequest):
    """
    Save session data to Google Drive
    
    Args:
        request: Session data to save
    
    Returns:
        Success confirmation with file ID
    """
    try:
        logger.info(f"Saving session for {request.user_id}")
        
        # Add timestamp
        session_data = request.session_data
        session_data['saved_at'] = datetime.now().isoformat()
        session_data['user_id'] = request.user_id
        
        # Save to Google Drive
        file_id = storage.save_session(session_data, request.user_id)
        
        # Save alert if triggered
        if session_data.get('alert_triggered', False):
            alert_id = alert_system.save_alert(session_data, request.user_id)
            logger.info(f"Alert saved: {alert_id}")
        
        logger.info(f"Session saved: {file_id}")
        return {
            "status": "success",
            "file_id": file_id,
            "message": "Session data saved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in save endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Save error: {str(e)}")


@app.get("/history/{user_id}")
async def get_history(user_id: str, limit: int = 10):
    """
    Retrieve session history for a user
    
    Args:
        user_id: User identifier
        limit: Number of recent sessions to retrieve
    
    Returns:
        List of recent sessions
    """
    try:
        logger.info(f"Fetching history for {user_id}")
        
        sessions = storage.get_user_sessions(user_id, limit)
        
        return {
            "user_id": user_id,
            "sessions": sessions,
            "count": len(sessions)
        }
        
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"History error: {str(e)}")


# Compatibility endpoint for existing frontend
@app.post("/predict")
async def predict(
    frame: UploadFile = File(...),
    voice: UploadFile = File(...)
):
    """Legacy endpoint for backward compatibility"""
    result = await analyze_emotion(frame, voice)
    return {
        "emotion": result.emotion,
        "message": result.message
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
