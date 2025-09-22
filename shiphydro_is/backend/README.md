# ShipHydro-IS Backend

ShipHydro-IS backend implements a modular fast-prototyping environment for ship hydrodynamics CFD workflows. The backend follows clean architecture principles with adapters for geometry, meshing, solvers, storage, and orchestration.

## Features

- Geometry DSL and import pipeline producing NURBS-inspired hull representations and STL outputs.
- Mock and external solver adapters with dry-run auditing.
- In-memory task orchestrator mimicking Celery semantics for demo usage.
- SQLite-backed metadata store with pluggable MinIO-compatible artifact storage.
- Surrogate modelling, optimization, and active learning APIs.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Running the demo

```
make demo
```

This command walks through geometry generation, mesh/solver mock execution, and persisting KPI results accessible from the frontend.

