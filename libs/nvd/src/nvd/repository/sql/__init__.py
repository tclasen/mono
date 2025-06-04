from sqlmodel import SQLModel, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from nvd.repository import BaseRepository
from nvd.types.base import BaseModel


class BaseSchema(SQLModel):
    pass


class BaseSqlRepository[ItemId, ItemModel: BaseModel, Schema: BaseSchema](BaseRepository[ItemId, ItemModel]):
    _schema: type[Schema]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, item: ItemModel) -> None:
        model = self._schema.model_validate(item.model_dump())
        self._session.add(model)

    async def load(self, key: ItemId) -> ItemModel | None:
        result = await self._session.get(self._schema, key)
        if result:
            return self._item_serializer.model_validate(result.model_dump())
        return None

    async def count(self) -> int:
        query = select(func.count()).select_from(self._schema)
        result = await self._session.exec(query)
        return result.one()
