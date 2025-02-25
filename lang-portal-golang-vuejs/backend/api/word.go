package api

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgtype"
)

type createWordRequest struct {
	Malay   string         `json:"malay" binding:"required"`
	Jawi    string         `json:"jawi" binding:"required"`
	English string         `json:"english" binding:"required"`
	Parts   map[string]any `json:"parts" binding:"required"`
}

type updateWordRequest struct {
	Malay   string         `json:"malay" binding:"required"`
	Jawi    string         `json:"jawi" binding:"required"`
	English string         `json:"english" binding:"required"`
	Parts   map[string]any `json:"parts" binding:"required"`
}

// listWords returns a list of all words with optional filtering
func (server *Server) listWords(ctx *gin.Context) {
	var limit int32 = 10
	var offset int32 = 0
	searchQuery := ctx.Query("q")

	// Parse query parameters
	if limitStr := ctx.Query("limit"); limitStr != "" {
		if val, err := strconv.Atoi(limitStr); err == nil {
			limit = int32(val)
		}
	}

	if offsetStr := ctx.Query("offset"); offsetStr != "" {
		if val, err := strconv.Atoi(offsetStr); err == nil {
			offset = int32(val)
		}
	}

	arg := db.ListWordsParams{
		Limit:  limit,
		Offset: offset,
		SearchQuery: pgtype.Text{
			String: searchQuery,
			Valid:  searchQuery != "",
		},
	}

	words, err := server.store.ListWords(ctx, arg)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, words)
}

// getWord returns a specific word by ID
func (server *Server) getWord(ctx *gin.Context) {
	id, err := strconv.Atoi(ctx.Param("id"))
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	log.Printf("Received request to get word with ID: %d", id)
	log.Printf("Incoming request to get word with query params: %+v", ctx.Request.URL.Query())
	log.Printf("Incoming request to get word with params: %+v", ctx.Params)

	word, err := server.store.GetWord(ctx, int32(id))
	if err != nil {
		if err.Error() == "no rows in result set" {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "word not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, word)
}

// createWord creates a new word
func (server *Server) createWord(ctx *gin.Context) {
	var req createWordRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	partsJSON, err := json.Marshal(req.Parts)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	word, err := server.store.CreateWord(ctx, db.CreateWordParams{
		Malay:   req.Malay,
		Jawi:    req.Jawi,
		English: req.English,
		Parts:   partsJSON,
	})

	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusCreated, word)
}

// updateWord updates an existing word
func (server *Server) updateWord(ctx *gin.Context) {
	id, err := strconv.Atoi(ctx.Param("id"))
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	var req updateWordRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	partsJSON, err := json.Marshal(req.Parts)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Get existing word
	_, err = server.store.GetWord(ctx, int32(id))
	if err != nil {
		if err == sql.ErrNoRows {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "word not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Update only provided fields
	params := db.UpdateWordParams{
		ID:      int32(id),
		Malay:   req.Malay,
		Jawi:    req.Jawi,
		English: req.English,
		Parts:   partsJSON,
	}

	word, err := server.store.UpdateWord(ctx, params)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, word)
}

// deleteWord deletes a word by ID
func (server *Server) deleteWord(ctx *gin.Context) {
	id, err := strconv.Atoi(ctx.Param("id"))
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	// First check if the word exists
	_, err = server.store.GetWord(ctx, int32(id))
	if err != nil {
		if err.Error() == "no rows in result set" {
			ctx.JSON(http.StatusNotFound, gin.H{"error": "word not found"})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	err = server.store.DeleteWord(ctx, int32(id))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "word deleted successfully"})
}
