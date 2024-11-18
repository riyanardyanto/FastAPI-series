from .models import User
from .schemas import UserCreateModel
from .utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user_by_email(self, session: AsyncSession, email: str):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, session: AsyncSession, email: str):
        user = await self.get_user_by_email(session, email)
        return bool(user)

    async def create_user(self, session: AsyncSession, user_data: UserCreateModel):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user
