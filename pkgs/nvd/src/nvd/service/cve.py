from sqlmodel.ext.asyncio.session import AsyncSession

from nvd.repository.nist_api.cve import CveNistapiRepository, CvePage
from nvd.repository.sql.cve import CveSchema, CveSqlRepository
from nvd.service import BaseService
from nvd.types.cve import Cve, CveId


class CveService(BaseService[CveId, Cve, CvePage, CveSchema]):
    def __init__(self, session: AsyncSession, nvd_api_key: str | None) -> None:
        self._sql_repo = CveSqlRepository(session)
        self._api_repo = CveNistapiRepository(nvd_api_key)

    async def get(self, key: CveId) -> Cve | None:
        result = None
        result = await self._sql_repo.get(key)
        if not result:
            result = await self._api_repo.get(key)
        return result
