import pytest
from nvd.types.cpe import Cpe23String


@pytest.mark.parametrize(
    "value",
    [
        "cpe:2.3:a:b:c:d:e:f:g:h:i:j:k",
        "cpe:2.3:a:3com:3cdaemon:-:*:*:*:*:*:*:*",
        "cpe:2.3:h:3com:3crwe454g72:-:*:*:*:*:*:*:*",
        "cpe:2.3:o:cisco:ios:12.4\\(11\\)xw6:*:*:*:*:*:*:*",
        "cpe:2.3:a:torproject:tor:0.1.1.10:alpha:*:*:*:*:*:*",
        "cpe:2.3:a:misterpark:hydrogen_water:1:*:*:*:*:android:*:*",
        "cpe:2.3:a:jenkins:script_security:1.1:*:*:*:*:jenkins:*:*",
        "cpe:2.3:a:nvidia:gpu_driver:310.44:-:*:*:esx:*:*:*",
        "cpe:2.3:a:bundler:bundler:1.3.0:pre:*:*:*:ruby:*:*",
    ],
)
def test_cpe_parser_roundtrip(value: str) -> None:
    cpe = Cpe23String.from_uri(value)
    assert value == str(cpe)
