package api

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

// GetStudyActivities returns a list of available study activities.
func GetStudyActivities(c *gin.Context) {
	// TODO: Implement logic to retrieve study activities
	c.JSON(http.StatusOK, gin.H{
		"items": []interface{}{
			map[string]interface{}{
				"id": 1,
				"name": "Vocabulary Quiz",
				"thumbnail_url": "https://example.com/thumbnail.jpg",
				"description": "Practice your vocabulary with flashcards",
			},
		},
		"pagination": map[string]interface{}{
			"current_page": 1,
			"total_pages": 5,
			"total_items": 100,
			"items_per_page": 100,
		},
	})
}

// GetStudyActivity returns details about a specific study activity.
func GetStudyActivity(c *gin.Context) {
	id := c.Param("id")
	// TODO: Implement logic to retrieve a specific study activity
	c.JSON(http.StatusOK, gin.H{
		"id": id,
		"name": "Basic Greetings",
		"stats": map[string]interface{}{
			"total_word_count": 20,
		},
	})
}
