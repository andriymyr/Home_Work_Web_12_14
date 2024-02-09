import os
import contextlib

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

db_username = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_name = os.environ.get("POSTGRES_DB")
domain = os.environ.get("POSTGRES_DOMAIN")
db_port = os.environ.get("POSTGRES_PORT")
DB_URL = (
    f"postgresql+asyncpg://{db_username}:{db_password}@{domain}:{db_port}/{db_name}"
)
#print("*" * 60)
#print(DB_URL)
#print("*" * 60)

GSSO_CLIENT_ID = os.environ.get("GSSO_CLIENT_ID")
GSSO_CLIENT_SECRET = os.environ.get("GSSO_CLIENT_SECRET")
secret_key = os.environ.get("secret_key")
SECRET_KEY_JWT = os.environ.get("SECRET_KEY_JWT")
ALGORITHM = os.environ.get("ALGORITHM")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_SERVER = os.environ.get("MAIL_SERVER")
REDIS_DOMAIN = os.environ.get("REDIS_DOMAIN")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
CLD_NAME = os.environ.get("CLD_NAME")
CLD_API_KEY = os.environ.get("CLD_API_KEY")
CLD_API_SECRET = os.environ.get("CLD_API_SECRET")
ACCOUNT_EXIST = "Account already exists!"

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
