from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


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
    publication_date: str
    page_count: int
    language: str
    create_at: datetime = Field(
        Column(pg.TIMESTAMP(timezone=True), default=datetime.now())
    )
    update_at: datetime = Field(
        Column(pg.TIMESTAMP(timezone=True), default=datetime.now())
    )

    def __repr__(self):
        return f"<Book {self.title}>"
