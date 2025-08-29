from typing import Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from file_validation import DocumentValidator

import uuid

#create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

doc_validator = DocumentValidator()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/single")
async def create_upload_singlefile(file: UploadFile = File(...)):
    
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

    return {
        "sucsess":True,
        "original_filename": file.filename,

        "stored_filename": unique_filename,

        "content_type": file.content_type,

        "size": file.size,

        "location": str(file_path)

    }
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}