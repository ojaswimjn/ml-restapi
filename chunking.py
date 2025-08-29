import re

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

def sentence_merge_chunking(text: str, max_len: int = 100, overlap: int = 20) -> List[str]:
    """
    Complementary chunking:
    - split by sentences
    - merge sentences into chunks with fixed max length
    - include overlap to preserve context
    """
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_len = 0
    
    for sentence in sentences:
        sentence_len = len(sentence)
        if current_len + sentence_len <= max_len:
            current_chunk.append(sentence)
            current_len += sentence_len
        else:
            chunks.append(" ".join(current_chunk))
            # add overlap sentences to new chunk
            current_chunk = current_chunk[-overlap//2:] if overlap > 0 else []
            current_chunk.append(sentence)
            current_len = sum(len(s) for s in current_chunk)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
    
text = """This is the first paragraph of the document.
It contains multiple sentences.

This is the second paragraph.
It also has multiple sentences for demonstration."""

chunks = document_based_chunking(text)
print(chunks)