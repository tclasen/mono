from typing import Annotated
from uuid import UUID

from sqlmodel import Field

from nvd.repository.sql import BaseSchema, BaseSqlRepository
from nvd.types.cpe import Cpe, CpeId


class CpeSchema(BaseSchema, table=True):
    __tablename__ = "cpe"

    id: Annotated[UUID, Field(primary_key=True)]


class CpeSqlRepository(BaseSqlRepository[CpeId, Cpe, CpeSchema]):
    _item_serializer = Cpe
    _schema = CpeSchema
