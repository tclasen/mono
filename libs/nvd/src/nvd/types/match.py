from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import NewType
from uuid import UUID

from nvd.types.base import BaseModel

MatchId = NewType("MatchId", UUID)


class Match(BaseModel):
    id: MatchId
    created: datetime
    last_modified: datetime
