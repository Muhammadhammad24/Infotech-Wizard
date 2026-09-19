from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.dependencies import get_chatbot_service
from app.api.routes import chat
from app.core.config import get_settings
from app.core.logging import logger
from app.models.requests import HealthCheckResponse
from app.services.chatbot import ChatbotService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifecycle."""
    # Startup
    logger.info(f"Starting {settings.project_name} v{__version__}")
    
    # Optionally warmup models on startup
    if not settings.debug:
        try:
            chatbot = get_chatbot_service()
            chatbot.warmup()
        except Exception as e:
            logger.error(f"Failed to warmup models: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    version=__version__,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix=settings.api_v1_prefix)


@app.get("/", response_model=HealthCheckResponse)
async def root(chatbot: ChatbotService = Depends(get_chatbot_service)):
    """Root endpoint - health check."""
    return HealthCheckResponse(
        status="ok",
        version=__version__,
        models_loaded=chatbot.is_ready()
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health(chatbot: ChatbotService = Depends(get_chatbot_service)):
    """Health check endpoint."""
    return HealthCheckResponse(
        status="ok",
        version=__version__,
        models_loaded=chatbot.is_ready()
    )