"""Illustrates use of the sqlalchemy.ext.asyncio.AsyncSession object
for asynchronous ORM use.

"""

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from data import config

from utils.db_api import TimedBaseModel, BaseModel
from utils.db_api.schemas import TG_Account, Person



async def async_main():
    """Main program function."""

    engine = create_async_engine(config.POSTGRES_URI, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    nikita = Person(name_or_nickname='Nikita_Ivanov')
    nikita_tg = TG_Account(username='npopok', id=654321, person=nikita)

    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all(
                [
                    nikita_tg
                ]
            )

        # for relationship loading, eager loading should be applied.
        stmt = select(Person).options(selectinload(Person.tg_account))

        print(stmt)

        # AsyncSession.execute() is used for 2.0 style ORM execution
        # (same as the synchronous API).
        # result = await session.execute(stmt)
        # print(result)
        #
        # # result is a buffered Result object.
        # for a1 in result.scalars():
        #     print(a1)
        #     for b1 in a1.bs:
        #         print(b1)
        #
        # # for streaming ORM results, AsyncSession.stream() may be used.
        result = await session.stream(stmt)
        print(result)
        #
        # # result is a streaming AsyncResult object.
        # async for a1 in result.scalars():
        #     print(a1)
        #     for b1 in a1.bs:
        #         print(b1)
        #
        # result = await session.execute(select(A).order_by(A.id))
        #
        # a1 = result.scalars().first()
        #
        # a1.data = "new data"

        await session.commit()

        await engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
