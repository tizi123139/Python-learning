from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession

ASYNC_DATABASE_URL ="mysql+aiomysql://tizi1234:Tizi6666@localhost:3306/news_app?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal= async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  #提交事务
        except Exception:
            await session.rollback()  #有异常
            raise
        finally:
            await session.close()  #关闭会话
