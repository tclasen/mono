from collections.abc import Sequence
from datetime import datetime
from typing import Annotated

from pydantic import Field

from nvd.repository.nist_api import BaseNistApiRepository, BasePage
from nvd.types.base import BaseModel
from nvd.types.cve import Cve, CveId


class CveModel(BaseModel):
    id: CveId
    published: datetime
    last_modified: Annotated[datetime, Field(alias="lastModified")]

    def to_cve(self) -> Cve:
        return Cve.model_validate(self.model_dump())


class CveRoot(BaseModel):
    cve: CveModel


class CvePage(BasePage):
    vulnerabilities: tuple[CveRoot, ...]


class CveNistapiRepository(BaseNistApiRepository[CveId, Cve, CvePage]):
    _base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    _item_key = "cveId"
    _item_serializer = Cve
    _page_serializer = CvePage

    def _items_from_page(self, page: CvePage) -> Sequence[Cve]:
        return [item.cve.to_cve() for item in page.vulnerabilities]
