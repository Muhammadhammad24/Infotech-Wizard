"""Build the FAISS index from the ticket metadata in data/.

The index file is large and machine-specific, so it is not committed. Run this
once after cloning, or whenever the metadata or embedding model changes:

    python -m scripts.build_index

Each ticket is embedded as "subject. body" with the configured sentence
transformer. Vectors are L2-normalised and stored in an inner-product index,
so search scores are cosine similarities in [-1, 1].
"""

import json
import pickle
from datetime import datetime, timezone
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

BATCH_SIZE = 256


def ticket_text(ticket: dict) -> str:
    subject = (ticket.get("subject") or "").strip()
    body = (ticket.get("body") or "").strip()
    return f"{subject}. {body}" if subject else body


def main() -> None:
    settings = get_settings()
    metadata_path = Path(settings.metadata_path)
    index_path = Path(settings.faiss_index_path)
    config_path = Path(settings.config_path)

    with metadata_path.open("rb") as f:
        tickets = pickle.load(f)
    print(f"Loaded {len(tickets)} tickets from {metadata_path}")

    model = SentenceTransformer(settings.embedding_model)
    vectors = model.encode(
        [ticket_text(t) for t in tickets],
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).astype(np.float32)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))

    config = {
        "embedding_model": settings.embedding_model,
        "embedding_dimension": int(vectors.shape[1]),
        "total_documents": len(tickets),
        "index_type": "FlatIP",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.1",
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {index.ntotal} vectors to {index_path}")


if __name__ == "__main__":
    main()
