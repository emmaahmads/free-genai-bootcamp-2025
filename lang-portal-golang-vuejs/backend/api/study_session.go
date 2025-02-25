package api

import (
	"net/http"
	"strconv"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgtype"
)

type createStudySessionRequest struct {
	GroupID         pgtype.Int4 `json:"group_id" binding:"required"`
	StudyActivityID pgtype.Int4 `json:"study_activity_id" binding:"required"`
}

type createReviewRequest struct {
	WordID  int32 `json:"word_id" binding:"required"`
	Correct bool  `json:"correct" binding:"required"`
}

// listStudySessions returns a list of all study sessions with pagination
func (server *Server) listStudySessions(ctx *gin.Context) {
	// Get pagination parameters with defaults
	limit := 10
	offset := 0

	if limitStr := ctx.DefaultQuery("limit", "10"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 {
			limit = l
		}
	}

	if offsetStr := ctx.DefaultQuery("offset", "0"); offsetStr != "" {
		if o, err := strconv.Atoi(offsetStr); err == nil && o >= 0 {
			offset = o
		}
	}

	sessions, err := server.store.ListStudySessions(ctx, db.ListStudySessionsParams{
		Limit:  int32(limit),
		Offset: int32(offset),
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, sessions)
}

// createStudySession creates a new study session
func (server *Server) createStudySession(ctx *gin.Context) {
	var req createStudySessionRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	session, err := server.store.CreateStudySession(ctx, db.CreateStudySessionParams{
		GroupID:         req.GroupID,
		StudyActivityID: req.StudyActivityID,
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusCreated, session)
}

// getSessionReviews returns all reviews for a specific study session
func (server *Server) getSessionReviews(ctx *gin.Context) {
	// Get session ID from URL parameter
	sessionID, err := strconv.ParseInt(ctx.Param("id"), 10, 32)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid session ID"})
		return
	}

	// Get pagination parameters with defaults
	limit := 10
	offset := 0

	if limitStr := ctx.DefaultQuery("limit", "10"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 {
			limit = l
		}
	}

	if offsetStr := ctx.DefaultQuery("offset", "0"); offsetStr != "" {
		if o, err := strconv.Atoi(offsetStr); err == nil && o >= 0 {
			offset = o
		}
	}

	reviews, err := server.store.GetSessionReviews(ctx, db.GetSessionReviewsParams{
		StudySessionID: pgtype.Int4{Int32: int32(sessionID), Valid: true},
		Limit:          int32(limit),
		Offset:         int32(offset),
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, reviews)
}

// createReview creates a new review for a study session
func (server *Server) createReview(ctx *gin.Context) {
	// Get session ID from URL parameter
	sessionID, err := strconv.ParseInt(ctx.Param("id"), 10, 32)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid session ID"})
		return
	}

	var req createReviewRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	review, err := server.store.CreateWordReview(ctx, db.CreateWordReviewParams{
		WordID:         pgtype.Int4{Int32: req.WordID, Valid: true},
		StudySessionID: pgtype.Int4{Int32: int32(sessionID), Valid: true},
		Correct:        req.Correct,
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusCreated, review)
}
