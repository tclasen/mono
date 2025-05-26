from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from nvd.service.cpe import CpeService
from nvd.service.cve import CveService
from nvd.service.match import MatchService
from nvd.types.cpe import Cpe, CpeId
from nvd.types.cve import Cve, CveId
from nvd.types.match import Match, MatchId

if TYPE_CHECKING:
    from sqlmodel.ext.asyncio.session import AsyncSession


class Nvd:
    def __init__(self, session: AsyncSession, nvd_api_key: str | None) -> None:
        self._cve_service = CveService(session, nvd_api_key)
        self._cpe_service = CpeService(session, nvd_api_key)
        self._match_service = MatchService(session, nvd_api_key)

    async def get_cve(self, cve_id: str) -> Cve | None:
        return await self._cve_service.get(CveId(cve_id))

    async def get_cpe(self, cpe_id: str) -> Cpe | None:
        return await self._cpe_service.get(CpeId(UUID(cpe_id)))

    async def get_match(self, match_id: str) -> Match | None:
        return await self._match_service.get(MatchId(UUID(match_id)))
