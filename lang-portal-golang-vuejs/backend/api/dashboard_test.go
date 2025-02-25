package api

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestGetDashboardStats(t *testing.T) {
	server, _, cleanup := setupTestServer(t)
	defer cleanup()

	testCases := []struct {
		name          string
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name: "SuccessfulResponse",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)

				var response map[string]interface{}
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)

				// Check that all required fields are present
				require.Contains(t, response, "success_rate")
				require.Contains(t, response, "total_study_sessions")
				require.Contains(t, response, "total_active_groups")
				require.Contains(t, response, "study_streak_days")

				// Check types of the fields
				require.IsType(t, float64(0), response["success_rate"])
				require.IsType(t, float64(0), response["total_study_sessions"])
				require.IsType(t, float64(0), response["total_active_groups"])
				require.IsType(t, float64(0), response["study_streak_days"])

				// Check value ranges
				successRate := response["success_rate"].(float64)
				require.GreaterOrEqual(t, successRate, float64(0))
				require.LessOrEqual(t, successRate, float64(100))

				totalStudySessions := response["total_study_sessions"].(float64)
				require.GreaterOrEqual(t, totalStudySessions, float64(0))

				totalActiveGroups := response["total_active_groups"].(float64)
				require.GreaterOrEqual(t, totalActiveGroups, float64(0))

				studyStreakDays := response["study_streak_days"].(float64)
				require.GreaterOrEqual(t, studyStreakDays, float64(0))
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			request, err := http.NewRequest(http.MethodGet, "/api/dashboard/stats", nil)
			require.NoError(t, err)

			recorder := httptest.NewRecorder()
			server.router.ServeHTTP(recorder, request)
			tc.checkResponse(t, recorder)
		})
	}
}
