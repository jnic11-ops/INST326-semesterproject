# text_processor.py
from base_processor import BaseProcessor
import re, string

class TextProcessor(BaseProcessor):
    def process(self, text: str):
        stopwords = {"the", "is", "in", "on", "and", "a", "of", "to"}
        text = re.sub(r"<.*?>", " ", text).lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        return " ".join([t for t in text.split() if t not in stopwords])
