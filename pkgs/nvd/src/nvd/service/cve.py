import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from nvd.repository.nist_api.cve import CveNistapiRepository, CvePage
from nvd.repository.sql.cve import CveSchema, CveSqlRepository
from nvd.service import BaseService
from nvd.types.cve import Cve, CveId

logger = logging.getLogger(__name__)


class CveService(BaseService[CveId, Cve, CvePage, CveSchema]):
    def __init__(self, session: AsyncSession, nvd_api_key: str | None) -> None:
        self._sql_repo = CveSqlRepository(session)
        self._api_repo = CveNistapiRepository(nvd_api_key)

    async def get(self, key: CveId) -> Cve | None:
        result = None
        result = await self._sql_repo.load(key)
        if not result:
            logger.info("Cache miss for CVE: %s", key)
            result = await self._api_repo.load(key)
            if result:
                await self._sql_repo.save(result)
        logger.info("Cache hit for CVE: %s", key)
        return result
