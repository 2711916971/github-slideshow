from __future__ import annotations

from pathlib import Path

from adapters.cfd.openfoam_writer import OpenFOAMCaseWriter
from app.schemas.common import CaseSpec, FluidProperties, GeometryHandle, TurbulenceModel


def _geometry_handle() -> GeometryHandle:
    return GeometryHandle(
        geometry_id="geom1",
        name="geom",
        hash="hash",
        artifact_path="/tmp/geom.stl",
        bbox=[0, 0, 0, 1, 1, 1],
        volume=10.0,
        waterplane_area=5.0,
        created_at="2023-01-01T00:00:00",
    )


def _case_spec() -> CaseSpec:
    return CaseSpec(
        geometry_id="geom1",
        speed=6.0,
        draft=3.0,
        froude_number=0.2,
        reynolds_number=1e7,
        fluid=FluidProperties(density=1025.0, viscosity=0.0012),
        turbulence_model=TurbulenceModel.K_OMEGA_SST,
        solver_options={},
    )


def test_case_writer(tmp_path: Path) -> None:
    writer = OpenFOAMCaseWriter(tmp_path)
    case_dir = writer.write_case(_geometry_handle(), _case_spec())
    assert (case_dir / "system" / "controlDict").exists()
