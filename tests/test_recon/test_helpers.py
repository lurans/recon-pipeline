import pytest
from unittest.mock import patch

from pipeline.recon.helpers import get_ip_address_version, get_scans, is_ip_address, meets_requirements
from pipeline.recon import AmassScan, MasscanScan, FullScan, HTBScan, SearchsploitScan, ThreadedNmapScan
from pipeline.recon.web import GobusterScan, SubjackScan, TKOSubsScan, AquatoneScan, WaybackurlsScan, WebanalyzeScan


def test_get_scans():
    with patch("pipeline.recon.helpers.meets_requirements"):
        scan_names = [
            AmassScan,
            GobusterScan,
            MasscanScan,
            SubjackScan,
            TKOSubsScan,
            AquatoneScan,
            FullScan,
            HTBScan,
            SearchsploitScan,
            ThreadedNmapScan,
            WebanalyzeScan,
            WaybackurlsScan,
        ]

        scans = get_scans()
        for scan in scan_names:
            if hasattr(scan, "requirements"):
                assert scan.__name__ in scans.keys()
            else:
                assert scan not in scans.keys()


@pytest.mark.parametrize(
    "requirements, exception, expected",
    [(["amass"], True, None), (["amass"], False, False), (["aquatone"], False, True)],
)
def test_meets_requirements(requirements, exception, expected):
    mdict = {"amass": {"installed": False}, "aquatone": {"installed": True}}
    with patch("pipeline.recon.helpers.tools", autospec=dict) as mtools:
        mtools.get.return_value = mdict.get(requirements[0])
        if exception:
            with pytest.raises(RuntimeError):
                meets_requirements(requirements, exception)
        else:
            assert meets_requirements(requirements, exception) is expected


@pytest.mark.parametrize(
    "test_input, expected",
    [("127.0.0.1", True), ("::1", True), ("abcd", False), ("", False), (-1, False), (1.0, False)],
)
def test_is_ip_address(test_input, expected):
    assert is_ip_address(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [("127.0.0.1", "4"), ("::1", "6"), ("abcd", None), ("", None), (-1, None), (1.0, None)]
)
def test_get_ip_address_version(test_input, expected):
    assert get_ip_address_version(test_input) == expected
