from typing import Annotated
from uuid import UUID

from sqlmodel import Field

from nvd.repository.sql import BaseSchema, BaseSqlRepository
from nvd.types.match import Match, MatchId


class MatchSchema(BaseSchema, table=True):
    __tablename__ = "match"

    id: Annotated[UUID, Field(primary_key=True)]


class MatchSqlRepository(BaseSqlRepository[MatchId, Match, MatchSchema]):
    _item_serializer = Match
    _schema = MatchSchema
