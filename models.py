# Импортируем нужные компоненты из SQLAlchemy

# ForeignKey используется для создания внешних ключей, связывающих таблицы в базе данных
# String представляет строковой тип данных для колонок таблиц
# BigInteger представляет числовой тип данных для колонок таблиц, работающий с большими числами
from sqlalchemy import ForeignKey, String, BigInteger

# Mapped используется для аннотации типов полей моделей SQLAlchemy
# DeclarativeBase - это базовый класс для всех моделей при использовании декларативного стиля SQLAlchemy
# mapped_column позволяет определять столбцы таблицы внутри модели, задавая их тип и параметры
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

# AsyncAttrs добавляет асинхронные атрибуты к базовому классу, упрощая работу с асинхронным кодом
# async_sessionmaker - фабрика для создания асинхронных сессий взаимодействия с базой данных
# create_async_engine создаёт асинхронный движок для работы с базой данных
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Task(Base):
    __tablename__ = 'tasks'

    id:Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)