package api

import (
	"net/http"
	"strconv"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/gin-gonic/gin"
)

// listStudyActivities returns a list of all study activities with pagination
func (s *Server) listStudyActivities(ctx *gin.Context) {
	// Get pagination parameters
	limit := 10 // default limit
	offset := 0 // default offset

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

	// Get study activities from database
	activities, err := s.store.ListStudyActivities(ctx, db.ListStudyActivitiesParams{
		Limit:  int32(limit),
		Offset: int32(offset),
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch study activities"})
		return
	}

	ctx.JSON(http.StatusOK, activities)
}

// getStudyActivity returns a specific study activity by ID
func (s *Server) getStudyActivity(ctx *gin.Context) {
	idStr := ctx.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "Invalid study activity ID"})
		return
	}

	activity, err := s.store.GetStudyActivity(ctx, int32(id))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch study activity"})
		return
	}

	ctx.JSON(http.StatusOK, activity)
}
