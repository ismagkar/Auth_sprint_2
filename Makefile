migrate:
	cd auth_service && alembic upgrade head

admin:
	docker compose exec auth_service bash -c "python scripts.py"

dev_up:
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

dev_down:
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

create_admin:
	docker-compose exec admin_service python manage.py createsuperuser
