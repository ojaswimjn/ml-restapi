import re
import nltk

nltk.download("punkt")
nltk.download("punkt_tab")

def document_based_chunking(text):
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    
    for paragraph in paragraphs:
        sentences = nltk.sent_tokenize(paragraph)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= 500:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    return chunks

def fixed_overlap_chunking(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
    
        start += chunk_size - overlap
    return chunks



