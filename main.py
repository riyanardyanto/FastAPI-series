from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Charles Scribner's Sons",
        "publication_date": "1925-04-10",
        "page_count": 180,
        "language": "English",
    }
]


class BookCreateModel(BaseModel):
    title: str
    author: str


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publication_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publication_date: str
    page_count: int
    language: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/greet")
async def greet(name: Optional[str] = None, age: Optional[int] = None):
    return {"message": f"Hello {name}", "age": age}


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {"title": book_data.title, "author": book_data.author}


# @app.get("/get_headers")
# async def get_headers(
#     accept: Optional[str] = fastapi.Header(None),
#     content_type: Optional[str] = fastapi.Header(None),
#     user_agent: Optional[str] = fastapi.Header(None),
#     host: Optional[str] = fastapi.Header(None),
# ):
#     request_headers = {}
#     request_headers["Accept"] = accept
#     request_headers["Content-Type"] = content_type
#     request_headers["User-Agent"] = user_agent
#     request_headers["Host"] = host
#     return request_headers


@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book):
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@app.get("/book/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch("/book/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update_data: BookUpdateModel):
    for book in books:
        if book["id"] == book_id:
            book.update(book_update_data.model_dump())
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
