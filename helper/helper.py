# utils/response_parser.py
import json
from logs.logger import logger

def extract_text_from_response(response) -> str:
    """Safely extracts text from any Gemini response structure."""
    try:
        content = response.content
        
        # Case 1 — plain string
        if isinstance(content, str):
            return content.strip()
        
        # Case 2 — list of dicts {"type": "text", "text": "..."}
        if isinstance(content, list) and len(content) > 0:
            item = content[0]
            if isinstance(item, dict):
                return (item.get("text") or item.get("content") or "").strip()
            if isinstance(item, str):
                return item.strip()
        
        # Case 3 — empty
        logger.error(f"Unexpected response structure → {type(content)}: {content}")
        return ""
        
    except Exception as e:
        logger.error(f"Response extraction failed → {e}")
        return ""