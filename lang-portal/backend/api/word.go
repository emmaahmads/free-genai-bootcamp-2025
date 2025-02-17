package api

import (
	"database/sql"
	"log"
	"net/http"
	"strconv"

	"github.com/jackc/pgx/v5/pgtype"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/gin-gonic/gin"
)

// listWords returns a list of all words with optional filtering
func (server *Server) listWords(c *gin.Context) {
	limit := 10 // default limit
	if limitStr := c.Query("limit"); limitStr != "" {
		if parsedLimit, err := strconv.Atoi(limitStr); err == nil {
			limit = parsedLimit
		}
	}

	offset := 0
	if offsetStr := c.Query("offset"); offsetStr != "" {
		if parsedOffset, err := strconv.Atoi(offsetStr); err == nil {
			offset = parsedOffset
		}
	}

	searchQuery := c.Query("q")

	log.Printf("Received request to list words with limit: %d, offset: %d, search query: %s", limit, offset, searchQuery)
	log.Printf("Incoming request to list words with query params: %+v", c.Request.URL.Query())

	words, err := server.store.ListWords(c, db.ListWordsParams{
		Limit:  int32(limit),
		Offset: int32(offset),
		SearchQuery: pgtype.Text{
			String: searchQuery,
			Valid:  searchQuery != "",
		},
	})

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, words)
}

// getWord returns a specific word by ID
func (server *Server) getWord(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	log.Printf("Received request to get word with ID: %d", id)
	log.Printf("Incoming request to get word with query params: %+v", c.Request.URL.Query())
	log.Printf("Incoming request to get word with params: %+v", c.Params)

	word, err := server.store.GetWord(c, int32(id))
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "word not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, word)
}
