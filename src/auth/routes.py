from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException


auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", response_model=UserModel)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    print(f"Email: {email} - {type(email)}", email)

    user_exists = await user_service.user_exists(email=email, session=session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists"
        )
    else:
        new_user = await user_service.create_user(session=session, user_data=user_data)
        return new_user
