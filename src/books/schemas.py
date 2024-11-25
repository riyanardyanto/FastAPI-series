from pydantic import BaseModel
from typing import List
from src.reviews.schemas import ReviewModel
import uuid
from datetime import datetime, date


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
    language: str
    create_at: datetime
    update_at: datetime


class BookDetailModel(Book):
    reviews: List[ReviewModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publication_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
    language: str
    create_at: datetime
    update_at: datetime
