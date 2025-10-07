"""
Alert System Module
Detects high stress/fatigue and generates alerts
"""

import logging
from datetime import datetime
from typing import Dict
import os
import json

logger = logging.getLogger(__name__)

class AlertSystem:
    """Alert detection and management system"""
    
    def __init__(self):
        """Initialize alert system with thresholds"""
        self.stress_emotions = ['stressed', 'anxious', 'sad']
        self.stress_threshold = 0.70  # 70% confidence
        self.alert_count = 0
        
    def check_alert(self, emotion: str, confidence: float) -> bool:
        """
        Check if alert should be triggered
        
        Args:
            emotion: Detected emotion
            confidence: Confidence level
            
        Returns:
            True if alert triggered, False otherwise
        """
        try:
            # Check if emotion indicates stress and confidence is high
            if emotion in self.stress_emotions and confidence >= self.stress_threshold:
                logger.warning(f"ALERT: High {emotion} detected with {confidence:.2f} confidence")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking alert: {e}")
            return False
    
    def save_alert(self, session_data: Dict, user_id: str) -> str:
        """
        Save alert report
        
        Args:
            session_data: Session information
            user_id: User identifier
            
        Returns:
            Alert ID or filepath
        """
        try:
            self.alert_count += 1
            
            # Create alert report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            alert_id = f"alert_{user_id}_{timestamp}"
            
            alert_data = {
                'alert_id': alert_id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'emotion': session_data.get('emotion', 'unknown'),
                'confidence': session_data.get('confidence', 0),
                'video_emotion': session_data.get('video_emotion', 'unknown'),
                'audio_emotion': session_data.get('audio_emotion', 'unknown'),
                'severity': self._calculate_severity(session_data),
                'recommendation': self._generate_recommendation(session_data)
            }
            
            # Save alert locally
            filepath = self._save_alert_locally(alert_id, alert_data)
            
            logger.info(f"Alert saved: {alert_id}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving alert: {e}")
            return ""
    
    def _calculate_severity(self, session_data: Dict) -> str:
        """Calculate alert severity level"""
        try:
            confidence = session_data.get('confidence', 0)
            
            if confidence >= 0.85:
                return "critical"
            elif confidence >= 0.75:
                return "high"
            else:
                return "medium"
                
        except Exception as e:
            logger.error(f"Error calculating severity: {e}")
            return "medium"
    
    def _generate_recommendation(self, session_data: Dict) -> str:
        """Generate recommendation based on alert"""
        emotion = session_data.get('emotion', 'unknown')
        
        recommendations = {
            'stressed': "Recommend immediate relaxation protocol. Consider breathing exercises and scheduled rest period.",
            'anxious': "Suggest anxiety management techniques. Review mission status and provide reassurance.",
            'sad': "Recommend psychological support session. Consider connection with support team or loved ones."
        }
        
        return recommendations.get(
            emotion,
            "Recommend monitoring and support session."
        )
    
    def _save_alert_locally(self, alert_id: str, alert_data: Dict) -> str:
        """Save alert to local storage"""
        try:
            # Create alerts directory
            alerts_dir = "data/alerts"
            os.makedirs(alerts_dir, exist_ok=True)
            
            # Save as JSON
            filename = f"{alert_id}.json"
            filepath = os.path.join(alerts_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(alert_data, indent=2, fp=f)
            
            # Also save as readable text
            txt_filename = f"{alert_id}.txt"
            txt_filepath = os.path.join(alerts_dir, txt_filename)
            
            with open(txt_filepath, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("MAITRI ALERT REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Alert ID: {alert_data['alert_id']}\n")
                f.write(f"User: {alert_data['user_id']}\n")
                f.write(f"Timestamp: {alert_data['timestamp']}\n")
                f.write(f"Severity: {alert_data['severity'].upper()}\n\n")
                f.write(f"Detected Emotion: {alert_data['emotion']}\n")
                f.write(f"Confidence: {alert_data['confidence']:.2%}\n")
                f.write(f"Video Emotion: {alert_data['video_emotion']}\n")
                f.write(f"Audio Emotion: {alert_data['audio_emotion']}\n\n")
                f.write("Recommendation:\n")
                f.write(f"{alert_data['recommendation']}\n\n")
                f.write("=" * 60 + "\n")
            
            logger.info(f"Alert saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving alert locally: {e}")
            return ""
