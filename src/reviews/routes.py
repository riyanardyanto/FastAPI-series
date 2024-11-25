from fastapi import APIRouter, Depends
from fastapi import status
from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from .services import ReviewService

rewiew_service = ReviewService()

reviews_router = APIRouter()


@reviews_router.post("/book/{book_uid}", status_code=status.HTTP_201_CREATED)
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await rewiew_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session,
    )
    return new_review
