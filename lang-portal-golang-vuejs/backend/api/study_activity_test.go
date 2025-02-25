package api

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/stretchr/testify/require"
)

func createTestStudyActivity(t *testing.T, store *db.Queries) db.StudyActivity {
	params := db.CreateStudyActivityParams{
		Name: "Test Activity",
		Url:  "https://example.com/test",
	}

	activity, err := store.CreateStudyActivity(context.Background(), params)
	require.NoError(t, err)
	return activity
}

func TestListStudyActivities(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	// Create test activities
	n := 3
	activities := make([]db.StudyActivity, n)
	for i := 0; i < n; i++ {
		activities[i] = createTestStudyActivity(t, store)
		defer store.DeleteStudyActivity(context.Background(), activities[i].ID)
	}

	testCases := []struct {
		name          string
		limit         string
		offset        string
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name:   "DefaultPagination",
			limit:  "",
			offset: "",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)

				var response []db.StudyActivity
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.NotEmpty(t, response)
				require.LessOrEqual(t, len(response), 10) // default limit is 10
			},
		},
		{
			name:   "CustomPagination",
			limit:  "2",
			offset: "1",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)

				var response []db.StudyActivity
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.LessOrEqual(t, len(response), 2)
			},
		},
		{
			name:   "InvalidLimit",
			limit:  "-1",
			offset: "0",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)
				var response []db.StudyActivity
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.LessOrEqual(t, len(response), 10) // should use default limit
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			url := "/api/study-activities"
			if tc.limit != "" || tc.offset != "" {
				url = fmt.Sprintf("/api/study-activities?limit=%s&offset=%s", tc.limit, tc.offset)
			}

			request, err := http.NewRequest(http.MethodGet, url, nil)
			require.NoError(t, err)

			recorder := httptest.NewRecorder()
			server.router.ServeHTTP(recorder, request)
			tc.checkResponse(t, recorder)
		})
	}
}

func TestGetStudyActivity(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	activity := createTestStudyActivity(t, store)
	defer store.DeleteStudyActivity(context.Background(), activity.ID)

	testCases := []struct {
		name          string
		activityID    string
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name:       "ExistingActivity",
			activityID: fmt.Sprintf("%d", activity.ID),
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)

				var response db.StudyActivity
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.Equal(t, activity.ID, response.ID)
				require.Equal(t, activity.Name, response.Name)
				require.Equal(t, activity.Url, response.Url)
			},
		},
		{
			name:       "NonExistentActivity",
			activityID: "999999",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusInternalServerError, recorder.Code)
			},
		},
		{
			name:       "InvalidID",
			activityID: "invalid",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest, recorder.Code)
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			url := fmt.Sprintf("/api/study-activities/%s", tc.activityID)
			request, err := http.NewRequest(http.MethodGet, url, nil)
			require.NoError(t, err)

			recorder := httptest.NewRecorder()
			server.router.ServeHTTP(recorder, request)
			tc.checkResponse(t, recorder)
		})
	}
}
