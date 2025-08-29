from pathlib import Path
from fastapi import UploadFile

class DocumentValidator:
    def __init__(self):  
        self.allowed_extensions = {'.pdf', '.txt'}

    async def validate_file(self, file: UploadFile) -> dict:
        """Check if the document file is valid"""
        result = {"valid": True, "errors": []}

        # Check if user selected a file
        if not file.filename or file.filename.strip() == "":
            result["valid"] = False
            result["errors"].append("No file selected")
            return result

        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            result["valid"] = False
            result["errors"].append(
                f"File extension '{file_ext}' not allowed. Use: .pdf or .txt"
            )

        return result
