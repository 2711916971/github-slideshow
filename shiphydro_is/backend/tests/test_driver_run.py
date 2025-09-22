from __future__ import annotations

from adapters.isd.base import CaseSpec
from adapters.isd.openfoam import OpenFOAMDriver


def test_driver_returns_mock_when_missing_binary(monkeypatch):
    driver = OpenFOAMDriver()
    spec = CaseSpec(name="demo", command=["nonexistent_binary"], environment={})
    result = driver.run_case(spec)
    assert result == "mock"
