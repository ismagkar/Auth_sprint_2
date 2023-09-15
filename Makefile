migrate:
	cd auth_service && alembic upgrade head

admin:
	docker compose exec auth_service bash -c "python scripts.py"

up_dev:
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

down_dev:
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v
