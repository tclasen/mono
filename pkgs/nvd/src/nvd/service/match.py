import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from nvd.repository.nist_api.match import MatchNistapiRepository, MatchPage
from nvd.repository.sql.match import MatchSchema, MatchSqlRepository
from nvd.service import BaseService
from nvd.types.match import Match, MatchId

logger = logging.getLogger(__name__)


class MatchService(BaseService[MatchId, Match, MatchPage, MatchSchema]):
    def __init__(self, session: AsyncSession, nvd_api_key: str | None) -> None:
        self._sql_repo = MatchSqlRepository(session)
        self._api_repo = MatchNistapiRepository(nvd_api_key)

    async def get(self, key: MatchId) -> Match | None:
        result = None
        result = await self._sql_repo.load(key)
        if not result:
            logger.info("Cache miss for Match: %s", key)
            result = await self._api_repo.load(key)
            if result:
                await self._sql_repo.save(result)
        logger.info("Cache hit for Match: %s", key)
        return result
