include test.env

export MODE=test

sqlc:
	sqlc generate
migrateup:
	goose -dir db/migrations $(DB_DRIVER) $(DB_URL) up
migratedown:
	goose -dir db/migrations $(DB_DRIVER) $(DB_URL) down
test:
	go test -v -cover -short ./...
server:
	go build -o server main.go
	./server


.PHONY: sqlc migrateup migratedown test server