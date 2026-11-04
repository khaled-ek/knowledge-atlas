#from fastapi import APIRouter
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Request
import jinja2
from fastapi.templating import Jinja2Templates
#from sqlalchemy.orm import Session

#from app.database import get_db
#from app.documents.models import Document
from pathlib import Path
from uuid import uuid4


webapp_router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

STORAGE_DIR = Path(f"{BASE_DIR}/storage/documents")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_TYPES = {
    ".pdf": "pdf",
    ".txt": "text",
    ".html": "html",
    ".htm": "html",
}

@webapp_router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )


@webapp_router.get("/upload-page")
async def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
    )



#router = APIRouter(prefix="/documents", tags=["documents"])

@webapp_router.post("/upload")
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):

    original_name = Path(file.filename or "").name
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT, and HTML files are allowed",
        )

    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}{extension}"
    destination = STORAGE_DIR / stored_name

    size = 0

    try:
        with destination.open("wb") as output:
            while chunk := await file.read(64 * 1024):
                size += len(chunk)

                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File exceeds the 10 MB limit",
                    )

                output.write(chunk)

        return templates.TemplateResponse(
            request=request,
            name="upload.html",
            context={
                "success_message": "File uploaded successfully!",
                "filename": original_name,
            },
        )

    except Exception:
        destination.unlink(missing_ok=True)
        raise

    finally:
        await file.close()
