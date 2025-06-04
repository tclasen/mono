import logging
from uuid import UUID

import pytest
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


async def test_fallback_to_local_remote(nvd: Nvd, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)

    cve_id = "CVE-1999-0095"

    caplog.clear()
    cached_item = await nvd.get_cve(cve_id)
    assert cached_item is not None
    assert len(caplog.records) > 0
    assert any(f"Cache miss for CVE: {cve_id}" in record.message for record in caplog.records)

    caplog.clear()
    cached_item = await nvd.get_cve(cve_id)
    assert cached_item is not None
    assert len(caplog.records) > 0
    assert any(f"Cache hit for CVE: {cve_id}" in record.message for record in caplog.records)


async def test_cache_counters(nvd: Nvd) -> None:
    assert await nvd.get_cpe("BAE41D20-D4AF-4AF0-AA7D-3BD04DA402A7")
    counts = await nvd.counts()
    del counts["cpe"]["remote"]
    del counts["cve"]["remote"]
    del counts["match"]["remote"]
    assert counts == {"cpe": {"local": 1}, "cve": {"local": 0}, "match": {"local": 0}}

    assert await nvd.get_cve("CVE-1999-0095")
    counts = await nvd.counts()
    del counts["cpe"]["remote"]
    del counts["cve"]["remote"]
    del counts["match"]["remote"]
    assert counts == {"cpe": {"local": 1}, "cve": {"local": 1}, "match": {"local": 0}}

    assert await nvd.get_match("36FBCF0F-8CEE-474C-8A04-5075AF53FAF4")
    counts = await nvd.counts()
    del counts["cpe"]["remote"]
    del counts["cve"]["remote"]
    del counts["match"]["remote"]
    assert counts == {"cpe": {"local": 1}, "cve": {"local": 1}, "match": {"local": 1}}
