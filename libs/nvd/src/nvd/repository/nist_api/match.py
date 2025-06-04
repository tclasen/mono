from collections.abc import Sequence
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from nvd.repository.nist_api import BaseNistApiRepository, BasePage
from nvd.types.base import BaseModel
from nvd.types.match import Match, MatchId


class MatchModel(BaseModel):
    id: Annotated[UUID, Field(alias="matchCriteriaId")]
    created: datetime
    last_modified: Annotated[datetime, Field(alias="lastModified")]

    def to_match(self) -> Match:
        return Match.model_validate(self.model_dump())


class MatchRoot(BaseModel):
    match_string: Annotated[MatchModel, Field(alias="matchString")]


class MatchPage(BasePage):
    match_strings: Annotated[tuple[MatchRoot, ...], Field(alias="matchStrings")]


class MatchNistapiRepository(BaseNistApiRepository[MatchId, Match, MatchPage]):
    _base_url = "https://services.nvd.nist.gov/rest/json/cpematch/2.0"
    _item_key = "matchCriteriaId"
    _item_serializer = Match
    _page_serializer = MatchPage

    def _items_from_page(self, page: MatchPage) -> Sequence[Match]:
        return [item.match_string.to_match() for item in page.match_strings]
