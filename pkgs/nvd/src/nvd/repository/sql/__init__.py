from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from nvd.repository import BaseRepository
from nvd.types.base import BaseModel


class BaseSchema(SQLModel):
    pass


class BaseSqlRepository[ItemId, ItemModel: BaseModel, Schema: BaseSchema](BaseRepository[ItemId, ItemModel]):
    _schema: type[Schema]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, key: ItemId) -> ItemModel | None:
        result = await self._session.get(self._schema, key)
        if result:
            return self._item_serializer.model_validate(result)
        return None
