from typing import Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pathlib import Path
from file_validation import DocumentValidator
from chunking import document_based_chunking
from encoding import chunk_encoding

import uuid, shutil, PyPDF2

#create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

doc_validator = DocumentValidator()


def extract_text_from_file(file_path: Path) -> str:
    if file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")

    elif file_path.suffix.lower() == ".pdf":
        text = ""
        with open (file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n\n"
        return text


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/single")
async def create_upload_singlefile(
    file: UploadFile = File(...),
    strategy: str = Query("document", regex="^(document|fixed)$"),

    ):
    
    validation = await doc_validator.validate_file(file)
    if not validation["valid"]:
        raise HTTPException (
            status_code = 400,
            detail = {
                "message": "File validation failed.",
                "errors": validation["errors"]
            }
        )
    
    #create unique filename while saving
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        status_code = 500,
        detail = f"Failed to save file: {str(e)}"

    chunks = []
    
    try:
        text = extract_text_from_file(file_path)
        if strategy == "document":
            chunks = document_based_chunking(text)

        else:  # strategy == "fixed"
            chunks = fixed_overlap_chunking(text, chunk_size=max_chunk_size, overlap=overlap)

        embedding = chunk_encoding(chunks)
        embedding_list = embedding.tolist()

    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to chunk file: {str(e)}")


    return {
        "sucsess":True,
        "original_filename": file.filename,

        "stored_filename": unique_filename,

        "content_type": file.content_type,

        "size": file.size,

        "location": str(file_path),
        "chunking": {
            "count": len(chunks),
        },
        "chunks": chunks,
        "embedding" : embedding_list

    }
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}