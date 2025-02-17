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

	// Dashboard routes
	// api.GET("/dashboard/last_study_session", server.getLastStudySession)
	// api.GET("/dashboard/study_progress", server.getStudyProgress)
	// api.GET("/dashboard/quick_stats", server.getQuickStats)

	// // Study Activities routes
	// api.GET("/study_activities", server.listStudyActivities)
	// api.GET("/study_activities/:id", server.getStudyActivity)
	// api.GET("/study_activities/:id/study_sessions", server.getActivityStudySessions)
	// api.POST("/study_activities", server.createStudySession)

	// Words routes
	api.GET("/words", server.listWords)
	api.GET("/words/:id", server.getWord)

	// // Groups routes
	// api.GET("/groups", server.listGroups)
	// api.GET("/groups/:id", server.getGroup)
	// api.GET("/groups/:id/words", server.getGroupWords)
	// api.GET("/groups/:id/study_sessions", server.getGroupStudySessions)

	// // Study Sessions routes
	// api.GET("/study_sessions", server.listStudySessions)
	// api.GET("/study_sessions/:id", server.getStudySession)
	// api.GET("/study_sessions/:id/words", server.getStudySessionWords)
	// api.POST("/study_sessions/:id/words/:word_id/review", server.createWordReview)

	// // System routes
	// api.POST("/reset_history", server.resetHistory)
	// api.POST("/full_reset", server.fullReset)
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
