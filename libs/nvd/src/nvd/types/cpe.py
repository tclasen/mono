from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import NewType
from uuid import UUID

from nvd.types.base import BaseModel

CpeId = NewType("CpeId", UUID)


class Cpe23String(BaseModel):
    part: str = "*"
    vendor: str = "*"
    product: str = "*"
    version: str = "*"
    update: str = "*"
    edition: str = "*"
    language: str = "*"
    sw_edition: str = "*"
    target_sw: str = "*"
    target_hw: str = "*"
    other: str = "*"

    @classmethod
    def from_uri(cls, value: str) -> Cpe23String:
        cpe_tag, cpe_version, *parts = value.split(":")
        if cpe_tag != "cpe":
            msg = f"Must start with 'cpe' as the first value. Found: {cpe_tag}"
            raise ValueError(msg)
        if cpe_version != "2.3":
            msg = f"CPE String parser only supports version 2.3. Found {cpe_version}"
            raise ValueError(msg)

        data = dict(
            zip(
                [
                    "part",
                    "vendor",
                    "product",
                    "version",
                    "update",
                    "edition",
                    "language",
                    "sw_edition",
                    "target_sw",
                    "target_hw",
                    "other",
                ],
                parts,
                strict=True,
            )
        )

        return Cpe23String(**data)

    def __str__(self) -> str:
        return (
            f"cpe:2.3:{self.part}:{self.vendor}"
            f":{self.product}:{self.version}:{self.update}"
            f":{self.edition}:{self.language}:{self.sw_edition}"
            f":{self.target_sw}:{self.target_hw}:{self.other}"
        )


class Cpe(BaseModel):
    id: CpeId
    created: datetime
    last_modified: datetime
