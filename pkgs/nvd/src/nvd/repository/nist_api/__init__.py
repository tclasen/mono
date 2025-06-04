import asyncio
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Annotated

from httpx import AsyncClient
from httpx import _status_codes as status_codes
from pydantic import Field

from nvd.repository import BaseRepository
from nvd.types.base import BaseModel


class BasePage(BaseModel):
    results_per_page: Annotated[int, Field(alias="resultsPerPage")]
    start_index: Annotated[int, Field(alias="startIndex")]
    total_results: Annotated[int, Field(alias="totalResults")]


class BaseNistApiRepository[ItemId, ItemModel: BaseModel, PageModel: BasePage](BaseRepository[ItemId, ItemModel], ABC):
    _base_url: str
    _page_serializer: type[PageModel]
    _item_key: str

    def __init__(self, nvd_api_key: str | None = None) -> None:
        self._headers = dict[str, str]()
        if nvd_api_key:
            self._headers["apiKey"] = nvd_api_key

    async def save(self, item: ItemModel) -> None:
        msg = "The NIST API is read-only"
        raise NotImplementedError(msg)

    async def load(self, key: ItemId) -> ItemModel | None:
        params = dict[str, str | int](
            {
                "resultsPerPage": 1,
                self._item_key: str(key),
            }
        )
        page = await self._get_page(**params)
        items = self._items_from_page(page)
        item = next((i for i in items), None)
        if item:
            return self._item_serializer.model_validate(item)
        return None

    async def _get_page(self, **params: str | int) -> PageModel:
        while True:
            async with AsyncClient(headers=self._headers) as client:
                response = await client.get(self._base_url, params=params)
            if response.status_code == status_codes.codes.TOO_MANY_REQUESTS:
                await asyncio.sleep(6)  # https://nvd.nist.gov/developers/start-here#Best-Practices
                continue
            response.raise_for_status()
            return self._page_serializer.model_validate_json(response.text)

    @abstractmethod
    def _items_from_page(self, page: PageModel) -> Sequence[ItemModel]:
        raise NotImplementedError

    async def count(self) -> int:
        params = {"resultsPerPage": 1}
        page = await self._get_page(**params)
        return page.total_results
