
import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware


import app.models
from app.web.routes import webapp_router
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="knowlege_atlas_session",
    max_age=60 * 60 * 24,
    same_site="lax",
    https_only=settings.APP_ENV == "production"
)

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)

app.include_router(webapp_router)

def main():
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()

