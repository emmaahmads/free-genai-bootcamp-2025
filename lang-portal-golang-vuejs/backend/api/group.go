package api

import (
	"database/sql"
	"net/http"
	"strconv"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5"
)

type createGroupRequest struct {
	Name string `json:"name" binding:"required"`
}

type updateGroupRequest struct {
	Name string `json:"name" binding:"required"`
}

// listGroups returns a list of all word groups with optional filtering
func (server *Server) listGroups(ctx *gin.Context) {
	limit := 10 // default limit
	offset := 0 // default offset

	if limitStr := ctx.Query("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil {
			limit = l
		}
	}

	if offsetStr := ctx.Query("offset"); offsetStr != "" {
		if o, err := strconv.Atoi(offsetStr); err == nil {
			offset = o
		}
	}

	groups, err := server.store.ListGroups(ctx, db.ListGroupsParams{
		Limit:  int32(limit),
		Offset: int32(offset),
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, groups)
}

// getGroup returns a specific group by ID
func (server *Server) getGroup(ctx *gin.Context) {
	id, err := strconv.ParseInt(ctx.Param("id"), 10, 32)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	// Get group directly from database to handle ErrNoRows correctly
	row := server.pool.QueryRow(ctx, "SELECT id, name, words_count, created_at, updated_at FROM groups WHERE id = $1", id)
	var group db.Group
	err = row.Scan(&group.ID, &group.Name, &group.WordsCount, &group.CreatedAt, &group.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "group not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, group)
}

// getGroupWords returns all words associated with a specific group
func (server *Server) getGroupWords(ctx *gin.Context) {
	id, err := strconv.ParseInt(ctx.Param("id"), 10, 32)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	// Check if group exists
	_, err = server.store.GetGroup(ctx, int32(id))
	if err != nil {
		if err == sql.ErrNoRows {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "group not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Get words for the group
	words, err := server.store.GetWordsByGroup(ctx, db.GetWordsByGroupParams{
		GroupID: int32(id),
		Limit:  100, // You might want to make this configurable
		Offset: 0,
	})
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, words)
}

// createGroup creates a new word group
func (server *Server) createGroup(ctx *gin.Context) {
	var req createGroupRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	group, err := server.store.CreateGroup(ctx, req.Name)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusCreated, group)
}

// updateGroup updates an existing group
func (server *Server) updateGroup(ctx *gin.Context) {
	id, err := strconv.ParseInt(ctx.Param("id"), 10, 32)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	var req updateGroupRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	group, err := server.store.UpdateGroup(ctx, db.UpdateGroupParams{
		ID:   int32(id),
		Name: req.Name,
	})
	if err != nil {
		if err == sql.ErrNoRows {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "group not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, group)
}

// deleteGroup deletes a group by ID
func (server *Server) deleteGroup(ctx *gin.Context) {
	id, err := strconv.ParseInt(ctx.Param("id"), 10, 32)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid group ID"})
		return
	}

	// Start a transaction
	tx, err := server.pool.Begin(ctx)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer tx.Rollback(ctx)

	// Check if group exists within transaction
	row := tx.QueryRow(ctx, "SELECT id FROM groups WHERE id = $1", id)
	var groupID int32
	err = row.Scan(&groupID)
	if err != nil {
		if err == pgx.ErrNoRows {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "group not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Delete group within transaction
	_, err = tx.Exec(ctx, "DELETE FROM groups WHERE id = $1", id)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Commit transaction
	err = tx.Commit(ctx)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "group deleted successfully"})
}
