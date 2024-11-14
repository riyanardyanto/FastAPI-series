from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid

from src.db.main import get_session
from src.db.main import engine


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: str = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = False
    created_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now),
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now),
    )

    def __repr__(self):
        return f"<User {self.username}>"
