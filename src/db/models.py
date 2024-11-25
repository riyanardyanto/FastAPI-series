from sqlmodel import SQLModel, Field, Column, Relationship
from typing import List, Optional
import sqlalchemy.dialects.postgresql as pg
import uuid
from src.db.main import get_session
from src.db.main import engine
from datetime import date, datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: str = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = False
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now),
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now),
    )
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Reviews"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    create_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now())
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now())
    )
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    create_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now())
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now())
    )
    book: Optional["Book"] = Relationship(back_populates="reviews")
    user: Optional["User"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
