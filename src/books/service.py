from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statements = select(Book).order_by(desc(Book.create_at))
        result = await session.exec(statements)
        return result.all()

    async def get_book(self, session: AsyncSession, book_uid: str):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        return result.first() if result else None

    async def create_book(self, session: AsyncSession, book_data: BookCreateModel):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.publication_date = datetime.strptime(
            book_data_dict["publication_date"], "%Y-%m-%d"
        )
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, session: AsyncSession, book_uid: str, update_data: BookUpdateModel
    ):
        existing_book = await self.get_book(session, book_uid)

        if existing_book:
            for key, value in update_data.model_dump().items():
                setattr(existing_book, key, value)

            await session.commit()
            return existing_book
        else:
            return None

    async def delete_book(self, session: AsyncSession, book_uid: str):
        book_to_delete = await self.get_book(session, book_uid)

        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None
