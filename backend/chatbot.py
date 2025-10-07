"""
MAITRI Chatbot Module
Provides empathetic conversational AI for astronauts
"""

import logging
from typing import Optional
import random

logger = logging.getLogger(__name__)

class MAITRIChatbot:
    """Empathetic AI chatbot for astronauts"""
    
    def __init__(self):
        """Initialize chatbot with conversation model"""
        self.model = None
        self.tokenizer = None
        self._load_model()
        self._init_responses()
        
    def _load_model(self):
        """Load DialoGPT or similar conversational model"""
        try:
            # Try to load transformers model
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                model_name = "microsoft/DialoGPT-small"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(model_name)
                logger.info("DialoGPT model loaded successfully")
            except ImportError:
                logger.warning("Transformers not available, using template responses")
                self.model = None
                
        except Exception as e:
            logger.error(f"Error loading chatbot model: {e}")
    
    def _init_responses(self):
        """Initialize empathetic response templates"""
        self.emotion_responses = {
            'stressed': [
                "I sense you might be feeling stressed. Remember, you're doing amazing work up there. Would you like to try a breathing exercise?",
                "It's completely normal to feel overwhelmed sometimes. Let's take a moment together. How can I help you relax?",
                "Your stress levels seem elevated. You're incredibly strong for handling everything you do. Want to talk about what's on your mind?"
            ],
            'anxious': [
                "I'm here with you. Feeling anxious in space is natural. Let's work through this together.",
                "Your safety is my priority. Everything is functioning normally. Would you like to review the mission status?",
                "Anxiety can be challenging, but you've trained for this. Let me help you find your center."
            ],
            'happy': [
                "It's wonderful to see you in good spirits! Your positive energy is inspiring.",
                "I'm so glad you're feeling well! Keep up that amazing attitude.",
                "Your happiness is contagious! How are things going with your tasks today?"
            ],
            'sad': [
                "I'm here for you. It's okay to feel sad sometimes, even in space. Want to talk about it?",
                "You're not alone up there. I'm always here to listen. What's weighing on your mind?",
                "Missing home is natural. Let me share something that might lift your spirits."
            ],
            'neutral': [
                "How are you feeling today? I'm here to support you in any way you need.",
                "Everything seems stable. Is there anything specific you'd like to discuss or any support you need?",
                "I'm monitoring your well-being. Feel free to share anything on your mind."
            ],
            'calm': [
                "You seem peaceful and centered. That's excellent! Keep maintaining this wonderful state.",
                "Your calm demeanor is admirable. Is there anything you'd like to do to maintain this feeling?",
                "It's great to see you so relaxed. How can I support your well-being today?"
            ]
        }
    
    def generate_emotion_response(self, emotion: str) -> str:
        """
        Generate an empathetic response based on detected emotion
        
        Args:
            emotion: Detected emotional state
            
        Returns:
            Empathetic message
        """
        try:
            # Get responses for this emotion
            responses = self.emotion_responses.get(
                emotion.lower(), 
                self.emotion_responses['neutral']
            )
            
            # Return random response from templates
            return random.choice(responses)
            
        except Exception as e:
            logger.error(f"Error generating emotion response: {e}")
            return "I'm here to support you. How are you feeling?"
    
    def generate_response(
        self, 
        message: str, 
        emotion_state: Optional[str] = None
    ) -> str:
        """
        Generate conversational response to user message
        
        Args:
            message: User's message
            emotion_state: Current emotional state (optional)
            
        Returns:
            AI-generated response
        """
        try:
            # If model is available, use it
            if self.model is not None and self.tokenizer is not None:
                return self._generate_model_response(message, emotion_state)
            
            # Otherwise, use template-based responses
            return self._generate_template_response(message, emotion_state)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm here to help. Can you tell me more about how you're feeling?"
    
    def _generate_model_response(
        self, 
        message: str, 
        emotion_state: Optional[str] = None
    ) -> str:
        """Generate response using DialoGPT model"""
        try:
            # Encode input
            input_ids = self.tokenizer.encode(
                message + self.tokenizer.eos_token, 
                return_tensors='pt'
            )
            
            # Generate response
            chat_history_ids = self.model.generate(
                input_ids,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=100,
                top_p=0.7,
                temperature=0.8
            )
            
            # Decode response
            response = self.tokenizer.decode(
                chat_history_ids[:, input_ids.shape[-1]:][0], 
                skip_special_tokens=True
            )
            
            # Add emotion-aware prefix if needed
            if emotion_state and emotion_state in ['stressed', 'anxious', 'sad']:
                response = f"I understand you're feeling {emotion_state}. {response}"
            
            return response
            
        except Exception as e:
            logger.error(f"Error in model generation: {e}")
            return self._generate_template_response(message, emotion_state)
    
    def _generate_template_response(
        self, 
        message: str, 
        emotion_state: Optional[str] = None
    ) -> str:
        """Generate response using templates"""
        
        message_lower = message.lower()
        
        # Check for specific keywords
        if any(word in message_lower for word in ['help', 'stress', 'overwhelm']):
            return "I'm here to support you. Would you like to try some relaxation techniques, or would you prefer to talk about what's bothering you?"
        
        elif any(word in message_lower for word in ['lonely', 'alone', 'miss']):
            return "I understand that being away from loved ones is difficult. Remember, you're part of an incredible mission, and many people are rooting for you. I'm always here to keep you company."
        
        elif any(word in message_lower for word in ['tired', 'exhaust', 'sleep']):
            return "Rest is crucial for your well-being. Have you been maintaining your sleep schedule? I can help you set up a better rest routine if needed."
        
        elif any(word in message_lower for word in ['thank', 'appreciate']):
            return "You're very welcome! Supporting you is my primary purpose. Is there anything else I can help you with?"
        
        elif any(word in message_lower for word in ['how are you', 'how is']):
            return "I'm functioning optimally and always ready to assist you! More importantly, how are YOU feeling today?"
        
        # Default responses based on emotion
        if emotion_state:
            return self.generate_emotion_response(emotion_state)
        
        # Generic friendly response
        return "I'm listening. Tell me more about what's on your mind, and I'll do my best to help."
