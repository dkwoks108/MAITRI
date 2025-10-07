"""
Emotion Analyzer Module
Handles video and audio emotion detection using FER and audio analysis
"""

import numpy as np
from PIL import Image
import io
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    """Analyzes emotions from video and audio inputs"""
    
    def __init__(self):
        """Initialize emotion analysis models"""
        self.video_model = None
        self.audio_model = None
        self._load_models()
        
    def _load_models(self):
        """Load FER and audio emotion models"""
        try:
            # Try to import FER for video emotion detection
            try:
                from fer import FER
                self.video_model = FER(mtcnn=True)
                logger.info("FER model loaded successfully")
            except ImportError:
                logger.warning("FER not available, using fallback")
                self.video_model = None
            
            # Audio emotion model (using simple heuristics for now)
            # In production, use SpeechBrain or similar
            logger.info("Audio emotion analyzer initialized")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def analyze_video(self, image_bytes: bytes) -> Tuple[str, float]:
        """
        Analyze emotion from video frame
        
        Args:
            image_bytes: Image data in bytes
            
        Returns:
            Tuple of (emotion, confidence)
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            if self.video_model is not None:
                # Use FER model
                result = self.video_model.detect_emotions(image_array)
                
                if result and len(result) > 0:
                    emotions = result[0]['emotions']
                    # Get dominant emotion
                    emotion = max(emotions, key=emotions.get)
                    confidence = emotions[emotion]
                    
                    logger.info(f"Video emotion detected: {emotion} ({confidence:.2f})")
                    return self._normalize_emotion(emotion), confidence
            
            # Fallback: return neutral with moderate confidence
            logger.info("Using fallback emotion detection")
            return "neutral", 0.6
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return "neutral", 0.5
    
    def analyze_audio(self, audio_bytes: bytes) -> Tuple[str, float]:
        """
        Analyze emotion from audio
        
        Args:
            audio_bytes: Audio data in bytes
            
        Returns:
            Tuple of (emotion, confidence)
        """
        try:
            # In a full implementation, use SpeechBrain or similar
            # For now, use simple heuristics based on audio characteristics
            
            # Analyze audio properties
            audio_length = len(audio_bytes)
            
            # Simple heuristic: longer audio might indicate more stress/talking
            if audio_length > 100000:
                return "stressed", 0.65
            elif audio_length < 50000:
                return "calm", 0.70
            else:
                return "neutral", 0.60
                
        except Exception as e:
            logger.error(f"Error analyzing audio: {e}")
            return "neutral", 0.5
    
    def fuse_emotions(
        self, 
        video_emotion: str, 
        video_conf: float,
        audio_emotion: str, 
        audio_conf: float
    ) -> Tuple[str, float]:
        """
        Fuse video and audio emotions using weighted average
        
        Args:
            video_emotion: Emotion from video
            video_conf: Video confidence
            audio_emotion: Emotion from audio
            audio_conf: Audio confidence
            
        Returns:
            Tuple of (final_emotion, confidence)
        """
        try:
            # Weight video more heavily (60% video, 40% audio)
            video_weight = 0.6
            audio_weight = 0.4
            
            # If emotions match, boost confidence
            if video_emotion == audio_emotion:
                confidence = (video_conf * video_weight + audio_conf * audio_weight) * 1.1
                confidence = min(confidence, 1.0)
                return video_emotion, confidence
            
            # If emotions differ, use higher confidence one
            if video_conf * video_weight > audio_conf * audio_weight:
                return video_emotion, video_conf * 0.9
            else:
                return audio_emotion, audio_conf * 0.9
                
        except Exception as e:
            logger.error(f"Error fusing emotions: {e}")
            return video_emotion, video_conf
    
    def _normalize_emotion(self, emotion: str) -> str:
        """
        Normalize emotion labels to standard set
        
        Args:
            emotion: Raw emotion label
            
        Returns:
            Normalized emotion label
        """
        # Map FER emotions to our standard set
        emotion_map = {
            'angry': 'stressed',
            'disgust': 'stressed',
            'fear': 'anxious',
            'happy': 'happy',
            'sad': 'sad',
            'surprise': 'alert',
            'neutral': 'neutral'
        }
        
        return emotion_map.get(emotion.lower(), emotion.lower())
