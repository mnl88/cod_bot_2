"""Illustrates use of the sqlalchemy.ext.asyncio.AsyncSession object
for asynchronous ORM use.

"""

import asyncio
import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from data import config

BaseModel = declarative_base()


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(True), server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime(True),
        default=datetime.datetime.now(),
        onupdate=datetime.datetime.now(),
        server_default=sa.func.now(),
    )


async def on_startup():

    engine = create_async_engine(config.POSTGRES_URI, echo=False)

    async with engine.begin() as conn:
        # await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


async def async_main(engine):
    """Main program function."""

    engine = create_async_engine(config.POSTGRES_URI, echo=False)

    async with engine.begin() as conn:
        # await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        # for relationship loading, eager loading should be applied.
        stmt = select(A).options(selectinload(A.bs))

        # AsyncSession.execute() is used for 2.0 style ORM execution
        # (same as the synchronous API).
        result = await session.execute(stmt)

        # result is a buffered Result object.
        for a1 in result.scalars():
            print(a1)
            for b1 in a1.bs:
                print(b1)

        # for streaming ORM results, AsyncSession.stream() may be used.
        result = await session.stream(stmt)

        # result is a streaming AsyncResult object.
        async for a1 in result.scalars():
            print(a1)
            for b1 in a1.bs:
                print(b1)

        result = await session.execute(select(A).order_by(A.id))

        a1 = result.scalars().first()

        a1.data = "new data"

        await session.commit()

        await engine.dispose()


# asyncio.run(async_main())