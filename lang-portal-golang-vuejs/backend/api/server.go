package api

import (
	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"
)

// Server serves HTTP requests for our language learning service.
type Server struct {
	store  *db.Queries
	pool   *pgxpool.Pool
	router *gin.Engine
}

// NewServer creates a new HTTP server and sets up routing.
func NewServer(pool *pgxpool.Pool) (*Server, error) {
	store := db.New(pool)
	server := &Server{
		store:  store,
		pool:   pool,
		router: gin.Default(),
	}

	// setup CORS
	server.router.Use(corsMiddleware())

	// setup routes
	server.setupRoutes()

	return server, nil
}

// setupRoutes sets up all the routes for our API
func (server *Server) setupRoutes() {
	// group all routes under /api
	api := server.router.Group("/api")

	// Words routes
	api.GET("/words", server.listWords)
	api.GET("/words/:id", server.getWord)
	api.POST("/words", server.createWord)
	api.PUT("/words/:id", server.updateWord)
	api.DELETE("/words/:id", server.deleteWord)

	// Groups routes
	api.GET("/groups", server.listGroups)
	api.GET("/groups/:id", server.getGroup)
	api.GET("/groups/:id/words", server.getGroupWords)
	api.POST("/groups", server.createGroup)
	api.PUT("/groups/:id", server.updateGroup)
	api.DELETE("/groups/:id", server.deleteGroup)

	// Study Sessions routes
	api.GET("/study-sessions", server.listStudySessions)
	api.POST("/study-sessions", server.createStudySession)
	api.GET("/study-sessions/:id/reviews", server.getSessionReviews)
	api.POST("/study-sessions/:id/reviews", server.createReview)

	// Study Activities routes
	api.GET("/study-activities", server.listStudyActivities)
	api.GET("/study-activities/:id", server.getStudyActivity)

	// Dashboard routes
	api.GET("/dashboard/stats", server.getDashboardStats)
}

// Start runs the HTTP server on a specific address.
func (server *Server) Start(address string) error {
	return server.router.Run(address)
}

// corsMiddleware handles CORS settings
func corsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}
