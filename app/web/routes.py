#from fastapi import APIRouter

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Request
import jinja2
from fastapi.templating import Jinja2Templates
#from sqlalchemy.orm import Session
from fastapi import Depends, Form
from fastapi.responses import RedirectResponse

#from app.database import get_db
#from app.documents.models import Document
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.schemas.auth import UserRegister
from app.core.security import hash_password,verify_password
from app.repositories.user_repository import UserRepository
from app.api.dependencies import get_db
from app.schemas.auth import UserLogin
from app.services.auth_service import AuthService


from starlette.datastructures import FormData

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

def register_form(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
) -> UserRegister:
    return UserRegister(
        full_name=full_name,
        email=email,
        password=password
    )

@webapp_router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="welcome.html",
    )


@webapp_router.get("/upload-page")
async def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
    )


@webapp_router.api_route("/register", methods=["GET", "POST"])
async def register(
    request: Request,
    db: Session = Depends(get_db)
):
    if request.method == "GET":
        return templates.TemplateResponse(
            request=request,
            name="register.html"
        )

    form_data = await request.form()

    try:

        #hashed_password = hash_password(user_data.password)
        user_data = UserRegister(
            full_name=form_data.get("full_name"),
            email=form_data.get("email"),
            password=form_data.get("password")
        )

    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Please check your registration details"},
            status_code = 422
        )

    # Chek whether the user already exists by their email
    existing_user = UserRepository.get_user_by_email(
        db=db,
        email=user_data.email
    )

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Email is already registered"},
            status_code=409
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Save user
    new_user = UserRepository.create_user(
        db=db,
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    # Redirect after successful registration
    return RedirectResponse(
        url="/login?registered=true",
        status_code=303
    )







@webapp_router.route("/login", methods=["GET", "POST"])
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    if request.method == "GET":
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={}
        )

    form_dat = await request.form()

    # Validate the submitted data
    try:
        user_data = UserLogin(
            email=form_dat.get("email"),
            password=form_dat.get("password")
        )

    except ValidationError:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Please enter valid credentials"},
            status_code=422
        )

    # Authenticate the user
    user = AuthService.authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )

    # Handle failed authentication
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Incorrect email or password"},
            status_code=401
        )

    # Authentication successful
    request.session.clear()
    request.session["user_id"] = str(user.id)

    # Redirect to the dashboard
    return RedirectResponse(
        url="/dashboard",
        status_code=303
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
