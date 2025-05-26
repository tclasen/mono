from typing import Annotated

from sqlmodel import Field

from nvd.repository.sql import BaseSchema, BaseSqlRepository
from nvd.types.cve import Cve, CveId


class CveSchema(BaseSchema, table=True):
    __tablename__ = "cve"

    id: Annotated[str, Field(primary_key=True)]


class CveSqlRepository(BaseSqlRepository[CveId, Cve, CveSchema]):
    _item_serializer = Cve
    _schema = CveSchema
