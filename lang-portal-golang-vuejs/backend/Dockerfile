FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the application
RUN go build -o server main.go

# Final stage
FROM alpine:latest

WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/server .

# Set environment variables
ENV DATABASE_URL="postgresql://superumi:superspecial@db:5432/lang_portal?sslmode=disable"

EXPOSE 8080

CMD ["./server"]
