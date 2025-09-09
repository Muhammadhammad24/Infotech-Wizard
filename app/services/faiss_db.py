import faiss
import pickle
import json
import numpy as np
from typing import Tuple, List, Dict, Any, Optional
from pathlib import Path
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()


class FAISSDatabase:
    """Service for managing FAISS index and metadata."""
    
    def __init__(
        self,
        index_path: Optional[str] = None,
        metadata_path: Optional[str] = None,
        config_path: Optional[str] = None
    ):
        self.index_path = Path(index_path or settings.faiss_index_path)
        self.metadata_path = Path(metadata_path or settings.metadata_path)
        self.config_path = Path(config_path or settings.config_path)
        
        self._index = None
        self._metadata = None
        self._config = None
        
    def _load_index(self) -> faiss.Index:
        """Load FAISS index."""
        if not self.index_path.exists():
            raise FileNotFoundError(f"FAISS index not found: {self.index_path}")
        
        logger.info(f"Loading FAISS index from {self.index_path}")
        return faiss.read_index(str(self.index_path))
    
    def _load_metadata(self) -> List[Dict[str, Any]]:
        """Load metadata."""
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found: {self.metadata_path}")
        
        logger.info(f"Loading metadata from {self.metadata_path}")
        with open(self.metadata_path, "rb") as f:
            return pickle.load(f)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        
        logger.info(f"Loading config from {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @property
    def index(self) -> faiss.Index:
        """Get FAISS index (lazy loaded)."""
        if self._index is None:
            self._index = self._load_index()
        return self._index
    
    @property
    def metadata(self) -> List[Dict[str, Any]]:
        """Get metadata (lazy loaded)."""
        if self._metadata is None:
            self._metadata = self._load_metadata()
        return self._metadata
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get config (lazy loaded)."""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 4
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Search for similar documents."""
        # Reshape if needed
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        scores, indices = self.index.search(query_embedding, k)
        return scores[0], indices[0]
    
    def get_metadata_by_indices(
        self,
        indices: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Get metadata for given indices."""
        results = []
        for idx in indices:
            if idx >= 0 and idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results
    
    def is_loaded(self) -> bool:
        """Check if database is loaded."""
        try:
            _ = self.index
            _ = self.metadata
            _ = self.config
            return True
        except Exception:
            return False