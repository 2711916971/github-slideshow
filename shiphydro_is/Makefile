.PHONY: demo backend-test lint type

VENV?=.venv

backend-test:
	cd backend && python -m pytest -q

lint:
	cd backend && ruff check .

type:
	cd backend && mypy app adapters core storage workers

demo:
	cd backend && python -m app.demo
