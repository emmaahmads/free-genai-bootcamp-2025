package main

import (
	"context"
	"log"
	"os"

	"github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/api"
	"github.com/jackc/pgx/v5/pgxpool"
)

func main() {
	// Load database configuration
	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		dbURL = "postgresql://superumi:superspecial@localhost:5432/lang_portal?sslmode=disable"
	}

	// Create connection pool
	pool, err := pgxpool.New(context.Background(), dbURL)
	if err != nil {
		log.Fatal("cannot connect to db:", err)
	}
	defer pool.Close()

	// Create server
	server, err := api.NewServer(pool)
	if err != nil {
		log.Fatal("cannot create server:", err)
	}

	// Start server
	err = server.Start(":8080")
	if err != nil {
		log.Fatal("cannot start server:", err)
	}
	log.Println("Server is running on port 8080")
}
