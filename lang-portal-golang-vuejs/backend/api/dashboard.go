package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// getDashboardStats returns statistics for the dashboard
func (s *Server) getDashboardStats(ctx *gin.Context) {
	// Get quick stats which includes success rate, study sessions, active groups, and streak
	stats, err := s.store.GetQuickStats(ctx)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch dashboard stats"})
		return
	}

	// TODO
	// // Get progress stats which includes total words studied vs available
	// progress, err := s.store.GetProgressStats(ctx)
	// if err != nil {
	// 	ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch progress stats"})
	// 	return
	// }

	// Combine all stats into a single response
	response := gin.H{
		"success_rate":         stats.SuccessRate,
		"total_study_sessions": stats.TotalStudySessions,
		"total_active_groups":  stats.TotalActiveGroups,
		"study_streak_days":    stats.StudyStreakDays,
		// "total_words_studied":  progress.TotalWordsStudied,
		// "total_words":         progress.TotalAvailableWords,
	}

	ctx.JSON(http.StatusOK, response)
}
