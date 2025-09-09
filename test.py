# test_services.py - Debug service initialization
import sys
sys.path.append('.')

from app.services.embeddings import EmbeddingService
from app.services.faiss_db import FAISSDatabase
from app.services.llm import LLMService
from app.services.chatbot import ChatbotService

print("🔍 Testing individual services...\n")

# Test Embedding Service
print("1. Testing Embedding Service...")
try:
    emb = EmbeddingService()
    test_embedding = emb.encode_query("test query")
    print(f"✅ Embedding service works! Shape: {test_embedding.shape}")
except Exception as e:
    print(f"❌ Embedding service failed: {e}")

# Test FAISS Database
print("\n2. Testing FAISS Database...")
try:
    db = FAISSDatabase()
    print(f"✅ FAISS index loaded: {db.index.ntotal} vectors")
    print(f"✅ Metadata loaded: {len(db.metadata)} documents")
    print(f"✅ Config loaded: {db.config}")
    print(f"✅ is_loaded(): {db.is_loaded()}")
except Exception as e:
    print(f"❌ FAISS database failed: {e}")
    import traceback
    traceback.print_exc()

# Test LLM Service
print("\n3. Testing LLM Service...")
try:
    llm = LLMService()
    print(f"✅ LLM service initialized")
    print(f"✅ is_loaded(): {llm.is_loaded()}")
    # Don't load the model yet, just check initialization
except Exception as e:
    print(f"❌ LLM service failed: {e}")

# Test Chatbot Service
print("\n4. Testing Chatbot Service...")
try:
    chatbot = ChatbotService()
    print(f"✅ Chatbot service initialized")
    print(f"✅ is_ready(): {chatbot.is_ready()}")
    
    # Check individual components
    print("\nChecking components:")
    print(f"  - Embeddings model loaded: {chatbot.embeddings.model is not None}")
    print(f"  - Database loaded: {chatbot.database.is_loaded()}")
    print(f"  - LLM loaded: {chatbot.llm.is_loaded()}")
    
except Exception as e:
    print(f"❌ Chatbot service failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("If all services show ✅, the API should work!")