from collections.abc import AsyncGenerator

from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel

from core.config import settings
from core.database import get_session
from core.dependencies import get_current_user
from main import app
from models.user import User

database_url = make_url(settings.database_url)

TEST_DATABASE_URL = database_url.set(database="train_ticket_test").render_as_string(
    hide_password=False
)

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    # 각 테스트에서 사용할 테스트용 DB 세션

    async with test_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    try:
        async with TestSessionLocal() as session:
            yield session
    finally:
        async with test_engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def test_user(test_session: AsyncSession) -> User:
    # 테스트용 사용자 생성

    user = User(
        email="test@example.com",
        hashed_password="test-password",
        name="테스트 사용자",
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def client(test_user: User) -> AsyncGenerator[AsyncClient, None]:
    # 테스트용 HTTP client

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        # 각 API 요청마다 독립적인 세션 생성
        async with TestSessionLocal() as session:
            yield session

    async def override_get_current_user() -> User:
        # 인증 과정은 테스트 대상이 아니므로 테스트 사용자로 대체
        return test_user

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as async_client:
            yield async_client
    finally:
        app.dependency_overrides.pop(get_session, None)
        app.dependency_overrides.pop(get_current_user, None)
