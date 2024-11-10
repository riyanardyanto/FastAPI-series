import fastapi
from typing import Optional
from pydantic import BaseModel

app = fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/greet")
async def greet(name: Optional[str] = None, age: Optional[int] = None):
    return {"message": f"Hello {name}", "age": age}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {"title": book_data.title, "author": book_data.author}


@app.get("/get_headers")
async def get_headers(
    accept: Optional[str] = fastapi.Header(None),
    content_type: Optional[str] = fastapi.Header(None),
    user_agent: Optional[str] = fastapi.Header(None),
    host: Optional[str] = fastapi.Header(None),
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    return request_headers
