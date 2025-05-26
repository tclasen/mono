from collections.abc import Sequence
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from nvd.repository.nist_api import BaseNistApiRepository, BasePage
from nvd.types.base import BaseModel
from nvd.types.cpe import Cpe, CpeId


class CpeModel(BaseModel):
    id: Annotated[UUID, Field(alias="cpeNameId")]
    created: datetime
    last_modified: Annotated[datetime, Field(alias="lastModified")]

    def to_cpe(self) -> Cpe:
        return Cpe.model_validate(self.model_dump())


class CpeRoot(BaseModel):
    cpe: CpeModel


class CpePage(BasePage):
    products: tuple[CpeRoot, ...]


class CpeNistapiRepository(BaseNistApiRepository[CpeId, Cpe, CpePage]):
    _base_url = "https://services.nvd.nist.gov/rest/json/cpes/2.0"
    _item_key = "cpeNameId"
    _item_serializer = Cpe
    _page_serializer = CpePage

    def _items_from_page(self, page: CpePage) -> Sequence[Cpe]:
        return [item.cpe.to_cpe() for item in page.products]
