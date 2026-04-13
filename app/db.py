from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import DATABASE_URL
from app.models import Base, User


engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


async def create_user(
    telegram_id: int,
    full_name: str,
    phone: str,
    language: str,
) -> User:
    async with SessionLocal() as session:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            phone=phone,
            language=language,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user