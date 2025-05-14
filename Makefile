update-deps:
	docker compose exec api python -m piptools compile -o requirements.txt pyproject.toml

install-deps:
	docker compose exec api pip-sync requirements.txt

local-up:
	docker compose up -d

status-processor:
	docker compose exec api python processor/processor.py

local-test:
	docker compose exec api pytest

local-age-group-test:
	docker compose exec age-group-api pytest
