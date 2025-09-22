from __future__ import annotations

import logging

from fastapi import FastAPI

from storage.database import init_db

from .api import jobs as jobs_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ShipHydro-IS")
app.include_router(jobs_router.router)


@app.on_event("startup")
async def startup_event() -> None:
    init_db()


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
