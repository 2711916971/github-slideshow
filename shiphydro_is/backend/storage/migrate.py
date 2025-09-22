from __future__ import annotations

import logging

from .database import init_db

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")


if __name__ == "__main__":
    main()
