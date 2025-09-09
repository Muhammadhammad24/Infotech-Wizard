from typing import List, Dict, Any, Set, Optional


def extract_password_context(
    candidates: List[Dict[str, Any]],
    password_keywords: Set[str],
    max_length: int = 500
) -> str:
    """Extract relevant context about passwords from search results."""
    
    def has_password_keyword(text: str) -> bool:
        """Check if text contains password-related keywords."""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in password_keywords)
    
    # Look for password-related content
    for candidate in candidates:
        subject = str(candidate.get("subject", ""))
        answer = str(candidate.get("answer", ""))
        
        if has_password_keyword(subject) or has_password_keyword(answer):
            # Combine subject and answer, truncate to max length
            context = f"{subject} — {answer}"
            if len(context) > max_length:
                context = context[:max_length] + "..."
            return context
    
    # No relevant context found
    return ""


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = " ".join(text.split())
    
    # Trim
    text = text.strip()
    
    return text