# example2.py - String utilities
import re
from typing import List

def clean_text(text: str) -> str:
    """Remove special characters"""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def split_words(text: str) -> List[str]:
    """Split text into words"""
    # FIXME: Handle empty strings
    return text.split()
