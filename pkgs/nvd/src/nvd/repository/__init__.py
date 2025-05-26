from abc import ABC, abstractmethod

from nvd.types.base import BaseModel


class BaseRepository[ItemId, ItemModel: BaseModel](ABC):
    _item_serializer: type[ItemModel]

    @abstractmethod
    async def get(self, key: ItemId) -> ItemModel | None:
        raise NotImplementedError
