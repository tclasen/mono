from abc import ABC, abstractmethod

from nvd.types.base import BaseModel


class BaseRepository[ItemId, ItemModel: BaseModel](ABC):
    _item_serializer: type[ItemModel]

    @abstractmethod
    async def load(self, key: ItemId) -> ItemModel | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, item: ItemModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError
