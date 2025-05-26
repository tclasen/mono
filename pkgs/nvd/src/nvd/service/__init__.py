from abc import ABC, abstractmethod

from nvd.repository.nist_api import BaseNistApiRepository, BasePage
from nvd.repository.sql import BaseSchema, BaseSqlRepository
from nvd.types.base import BaseModel


class BaseService[ItemId, ItemModel: BaseModel, PageModel: BasePage, Schema: BaseSchema](ABC):
    _sql_repo: BaseSqlRepository[ItemId, ItemModel, Schema]
    _api_repo: BaseNistApiRepository[ItemId, ItemModel, PageModel]

    @abstractmethod
    async def get(self, key: ItemId) -> ItemModel | None:
        raise NotImplementedError
