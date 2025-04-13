import os
import magic
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import patoolib
import tempfile

def process_file(file_path: str) -> str:
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        if file_type == "text/plain":
            with open(file_path, "r") as f:
                return f.read()
                
        elif file_type == "application/pdf":
            text = []
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text())
            return "\n".join(text)
            
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
            
        elif file_type.startswith("image/"):
            with Image.open(file_path) as img:
                return f"Image: {img.format}\nSize: {img.size}"
                
        elif file_type in ["application/zip", "application/x-rar-compressed"]:
            extract_dir = tempfile.mkdtemp()
            patoolib.extract_archive(file_path, outdir=extract_dir)
            return f"Extracted to: {extract_dir}"
            
        else:
            return f"Unsupported file type: {file_type}"
            
    except Exception as e:
        return f"Error processing file: {str(e)}"