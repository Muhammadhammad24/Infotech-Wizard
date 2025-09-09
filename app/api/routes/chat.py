from fastapi import APIRouter, Depends, HTTPException, status
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse, ErrorResponse
from app.api.dependencies import get_chatbot_service
from app.services.chatbot import ChatbotService
from app.core.logging import logger

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def chat(
    request: ChatRequest,
    chatbot: ChatbotService = Depends(get_chatbot_service)
) -> ChatResponse:
    """
    Process a chat query and return AI-generated response.
    
    - **query**: The user's question
    - **top_k**: Number of similar documents to retrieve (optional)
    - **max_tokens**: Maximum tokens for response generation (optional)
    """
    try:
        # Check readiness with detailed logging
        if not chatbot.is_ready():
            # Log detailed status for debugging
            logger.warning(f"Chatbot not ready - Embeddings: {chatbot.embeddings.model is not None}, "
                          f"Database: {chatbot.database.is_loaded()}")
            
            # Try to identify the specific issue
            error_details = []
            try:
                if chatbot.embeddings.model is None:
                    error_details.append("Embedding model not loaded")
            except Exception as e:
                error_details.append(f"Embedding check failed: {str(e)}")
            
            try:
                if not chatbot.database.is_loaded():
                    error_details.append("FAISS database not loaded")
            except Exception as e:
                error_details.append(f"Database check failed: {str(e)}")
            
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Chatbot service is not ready. Issues: {', '.join(error_details)}"
            )
        
        # Process query
        response = await chatbot.process_query(
            query=request.query,
            top_k=request.top_k,
            max_tokens=request.max_tokens
        )
        
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Chat processing error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@router.get("/health")
async def health_check(
    chatbot: ChatbotService = Depends(get_chatbot_service)
) -> dict:
    """Check if the chat service is healthy."""
    status_details = {
        "embeddings_loaded": False,
        "database_loaded": False,
        "llm_loaded": False
    }
    
    try:
        status_details["embeddings_loaded"] = chatbot.embeddings.model is not None
    except:
        pass
    
    try:
        status_details["database_loaded"] = chatbot.database.is_loaded()
    except:
        pass
    
    try:
        status_details["llm_loaded"] = chatbot.llm.is_loaded()
    except:
        pass
    
    return {
        "status": "healthy" if chatbot.is_ready() else "unhealthy",
        "service": "chat",
        "models_loaded": chatbot.is_ready(),
        "details": status_details
    }