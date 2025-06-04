from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import NewType

from nvd.types.base import BaseModel

CveId = NewType("CveId", str)


class Cve(BaseModel):
    id: CveId
    published: datetime
    last_modified: datetime
