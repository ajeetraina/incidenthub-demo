.PHONY: up down logs ps health test reset
up:
	docker compose up --build -d
down:
	docker compose down
logs:
	docker compose logs -f --tail=100
ps:
	docker compose ps
health:
	curl -fsS http://localhost:8000/api/health
test:
	python -m pytest -q tests/
reset:
	docker compose down -v
