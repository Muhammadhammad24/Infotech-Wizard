import time
import numpy as np
from typing import Optional, List, Dict, Any
from app.services.embeddings import EmbeddingService
from app.services.faiss_db import FAISSDatabase
from app.services.llm import LLMService
from app.utils.text_processing import extract_password_context
from app.models.responses import ChatResponse, SearchResult
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()


class ChatbotService:
    """Main chatbot orchestration service."""
    
    def __init__(self):
        self.embeddings = EmbeddingService()
        self.database = FAISSDatabase()
        self.llm = LLMService()
        
    def _perform_search(
        self,
        query: str,
        top_k: int
    ) -> tuple[List[Dict[str, Any]], np.ndarray, np.ndarray]:
        """Perform similarity search."""
        # Generate query embedding
        query_embedding = self.embeddings.encode_query(query)
        
        # Search FAISS
        scores, indices = self.database.search(query_embedding, k=top_k)
        
        # Get metadata
        results = []
        for score, idx in zip(scores, indices):
            if idx >= 0:
                metadata = self.database.metadata[idx]
                results.append({
                    **metadata,
                    "score": float(score)
                })
        
        return results, scores, indices
    
    def _prepare_search_results(
        self,
        results: List[Dict[str, Any]]
    ) -> List[SearchResult]:
        """Convert search results to response format."""
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                subject=result.get("subject", ""),
                answer=result.get("answer", ""),
                score=result.get("score", 0.0),
                metadata=result
            ))
        return search_results
    
    async def process_query(
        self,
        query: str,
        top_k: Optional[int] = None,
        max_tokens: Optional[int] = None
    ) -> ChatResponse:
        """Process a chat query and return response."""
        start_time = time.time()
        
        # Use defaults if not provided
        top_k = top_k or settings.top_k_results
        max_tokens = max_tokens or settings.max_tokens
        
        logger.info(f"Processing query: {query[:100]}...")
        
        try:
            # Perform search
            results, scores, indices = self._perform_search(query, top_k)
            
            # Extract context
            context = extract_password_context(
                results,
                settings.password_keywords
            )
            
            # Build messages
            messages = self.llm.build_messages(query, context)
            
            # Generate response
            response_text = self.llm.generate(messages, max_tokens)
            
            # Prepare response
            processing_time = time.time() - start_time
            
            return ChatResponse(
                response=response_text,
                query=query,
                context_used=context if context else None,
                search_results=self._prepare_search_results(results),
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            raise
    
    def warmup(self):
        """Warmup models by loading them."""
        logger.info("Warming up models...")
        
        # Load all models
        _ = self.embeddings.model
        _ = self.database.index
        _ = self.llm.model
        
        logger.info("✅ All models warmed up")
    
    def is_ready(self) -> bool:
        """Check if all services are ready."""
        try:
            return (
                self.embeddings.model is not None and
                self.database.is_loaded() #and
                #self.llm.is_loaded()
            )
        except Exception:
            return False