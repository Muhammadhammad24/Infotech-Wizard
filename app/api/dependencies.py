from typing import Generator
from app.services.chatbot import ChatbotService
from app.core.logging import logger

# Global chatbot instance
_chatbot_service = None


def get_chatbot_service() -> ChatbotService:
    """Get or create chatbot service instance."""
    global _chatbot_service
    
    if _chatbot_service is None:
        logger.info("Creating chatbot service instance...")
        _chatbot_service = ChatbotService()
        
        # Optionally warmup on first creation
        # _chatbot_service.warmup()
    
    return _chatbot_service