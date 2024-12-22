up:
	docker compose up -d

build:
	docker compose build --no-cache

down:
	docker compose down --remove-orphans --volumes --rmi all