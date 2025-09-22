from __future__ import annotations

from adapters.isd.base import CaseSpec
from adapters.isd.openfoam import OpenFOAMDriver


def test_openfoam_dry_run():
    driver = OpenFOAMDriver()
    spec = CaseSpec(name="demo", command=["simpleFoam", "-help"], environment={})
    dry = driver.dry_run(spec)
    assert dry.commands[0] == "simpleFoam -help"
