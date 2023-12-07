DB_DOCKER_CONTAINER=coffeeapi_container
DB_NAME=coffeedb
BINARY_NAME=coffeeapi

postgres:
	docker run --name  ${DB_DOCKER_CONTAINER} -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password -d postgres:12-alpine

createdb:
	docker exec -it ${DB_DOCKER_CONTAINER} createdb --username=root --owner=root ${DB_NAME}

create_migrations:
	sqlx migrate add -r init

run:
	go run cmd/server/main.go