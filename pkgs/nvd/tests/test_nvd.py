from uuid import UUID

from nvd import Nvd


def test_nvd_construction(nvd: Nvd) -> None:
    assert nvd


async def test_get_single_cve(nvd: Nvd) -> None:
    cve_id = "CVE-1999-0095"
    cve = await nvd.get_cve(cve_id)
    assert cve
    assert cve.id == cve_id
    assert cve.published.isoformat() == "1988-10-01T04:00:00"
    assert cve.last_modified >= cve.published


async def test_get_single_cpe(nvd: Nvd) -> None:
    cpe_id = "BAE41D20-D4AF-4AF0-AA7D-3BD04DA402A7"
    cpe_id_uuid = UUID(cpe_id)
    cpe = await nvd.get_cpe(cpe_id)
    assert cpe
    assert cpe.id == cpe_id_uuid
    assert cpe.created.isoformat() == "2007-08-23T21:05:57.937000"
    assert cpe.last_modified >= cpe.created


async def test_get_single_match(nvd: Nvd) -> None:
    match_id = "36FBCF0F-8CEE-474C-8A04-5075AF53FAF4"
    match_id_uuid = UUID(match_id)
    match = await nvd.get_match(match_id)
    assert match
    assert match.id == match_id_uuid
    assert match.created.isoformat() == "2019-06-17T09:16:33.960000"
    assert match.last_modified >= match.created
