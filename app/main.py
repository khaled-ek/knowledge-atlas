
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web.routes import webapp_router
from fastapi.templating import Jinja2Templates
from pathlib import Path


app = FastAPI()

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "teplates"
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
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()

