from sqlmodel.ext.asyncio.session import AsyncSession

from nvd.repository.nist_api.cpe import CpeNistapiRepository, CpePage
from nvd.repository.sql.cpe import CpeSchema, CpeSqlRepository
from nvd.service import BaseService
from nvd.types.cpe import Cpe, CpeId


class CpeService(BaseService[CpeId, Cpe, CpePage, CpeSchema]):
    def __init__(self, session: AsyncSession, nvd_api_key: str | None) -> None:
        self._sql_repo = CpeSqlRepository(session)
        self._api_repo = CpeNistapiRepository(nvd_api_key)

    async def get(self, key: CpeId) -> Cpe | None:
        result = None
        result = await self._sql_repo.get(key)
        if not result:
            result = await self._api_repo.get(key)
        return result
