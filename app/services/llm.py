import torch
import re
from typing import List, Dict, Optional
from transformers import pipeline
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()


class LLMService:
    """Service for managing the TinyLlama LLM."""
    
    def __init__(self, model_id: Optional[str] = None):
        self.model_id = model_id or settings.llm_model_id
        self._pipeline = None
        
    @property
    def pipeline(self):
        """Lazy load pipeline."""
        if self._pipeline is None:
            logger.info(f"Loading LLM pipeline: {self.model_id}")
            self._pipeline = pipeline(
                "text-generation",
                model=self.model_id,
                torch_dtype=torch.bfloat16,
                device_map="auto"
            )
            logger.info("✅ LLM pipeline loaded")
        return self._pipeline
    
    def build_messages(
        self,
        question: str,
        context_snippet: str = ""
    ) -> List[Dict[str, str]]:
        """Build chat messages."""
        system_prompt = (
            "You are an IT helpdesk assistant.\n"
            "Rules: Answer ONLY in English. Be concise. Use clear bullet points.\n"
            "If the provided context is irrelevant or empty, answer with standard best-practice steps.\n"
            "Do NOT mention purchases, receipts, or unrelated items."
        )
        
        user_prompt = (
            f"Question: {question}\n\n"
            f"Context (may be empty or unrelated):\n```{context_snippet}```\n\n"
            "Please provide a short, actionable answer with 3–5 bullet points."
        )
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        max_new_tokens: int = 130
    ) -> str:
        """Generate response from messages."""
        # Apply chat template
        prompt = self.pipeline.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Generate
        outputs = self.pipeline(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=False,  # Deterministic for consistency
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            pad_token_id=self.pipeline.tokenizer.pad_token_id,
            eos_token_id=self.pipeline.tokenizer.eos_token_id,
        )
        
        # Extract generated text (remove the prompt)
        generated_text = outputs[0]["generated_text"]
        # Remove the prompt part to get only the response
        if prompt in generated_text:
            generated_text = generated_text[len(prompt):].strip()
        
        # Clean output (ASCII only to avoid encoding issues)
        generated_text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", generated_text)
        
        # Remove any remaining template tokens
        generated_text = re.sub(r"<\|.*?\|>", "", generated_text).strip()
        generated_text = re.sub(r"</s>", "", generated_text).strip()
        
        return generated_text
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._pipeline is not None