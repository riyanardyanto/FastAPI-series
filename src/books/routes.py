from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from typing import List

book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
):
    new_book = await book_service.create_book(session, book_data)
    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(session, book_uid)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch(
    "/{book_uid}",
    response_model=BookUpdateModel,
)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_book = await book_service.update_book(session, book_uid, book_update_data)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.delete("/{book_uid}", status_code=status.HTTP_200_OK)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
):
    book_to_delete = book_service.delete_book(session, book_uid)

    if book_to_delete:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
