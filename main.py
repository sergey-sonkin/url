import string
import random
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener", description="A simple URL shortening service")
templates = Jinja2Templates(directory="templates")

url_database: Dict[str, str] = {}


class URLRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str
    original_url: str


def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@app.post("/shorten", response_model=URLResponse)
async def shorten_url(url_request: URLRequest):
    original_url = str(url_request.url)

    for code, existing_url in url_database.items():
        if existing_url == original_url:
            return URLResponse(short_url=code, original_url=original_url)

    short_code = generate_short_code()
    while short_code in url_database:
        short_code = generate_short_code()

    url_database[short_code] = original_url
    return URLResponse(short_url=short_code, original_url=original_url)


@app.get("/{short_code}")
async def redirect_to_url(short_code: str):
    if short_code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")

    original_url = url_database[short_code]
    return RedirectResponse(url=original_url, status_code=301)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
async def api_root():
    return {"message": "URL Shortener API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
