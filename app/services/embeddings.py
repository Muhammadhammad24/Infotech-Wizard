from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()


class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.embedding_model
        self._model = None
        
    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the embedding model."""
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully")
        return self._model
    
    def encode(self, texts: List[str], normalize: bool = True) -> np.ndarray:
        """Encode texts to embeddings."""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=False
        )
        return embeddings.astype("float32")
    
    def encode_query(self, query: str) -> np.ndarray:
        """Encode a single query."""
        return self.encode([query])[0]