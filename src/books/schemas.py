from pydantic import BaseModel


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
