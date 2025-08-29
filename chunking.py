import re
import nltk


def document_based_chunking(text):
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    
    for paragraph in paragraphs:
        sentences = nltk.sent_tokenize(paragraph)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= 100:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    return chunks

def fixed_overlap_chunking(text, chunk_size=100, overlap=20):
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



