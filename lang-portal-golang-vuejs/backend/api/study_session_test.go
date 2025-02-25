package api

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	db "github.com/emmaahmads/free-genai-bootcamp-2025/lang-portal/backend/db/sqlc"
	"github.com/jackc/pgx/v5/pgtype"
	"github.com/stretchr/testify/require"
)

func TestStudySessionEndpoints(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	// Clean up any existing data
	_, err := server.pool.Exec(context.Background(), `
		TRUNCATE word_review_items CASCADE;
		TRUNCATE study_sessions CASCADE;
		TRUNCATE study_activities CASCADE;
		TRUNCATE groups CASCADE;
		TRUNCATE words CASCADE;
	`)
	require.NoError(t, err)

	// Create test group and study activity
	var group struct {
		ID   int32  `json:"id"`
		Name string `json:"name"`
	}
	createGroupReq := createGroupRequest{
		Name: "Test Group",
	}
	body, err := json.Marshal(createGroupReq)
	require.NoError(t, err)
	w := httptest.NewRecorder()
	req, _ := http.NewRequest(http.MethodPost, "/api/groups", bytes.NewReader(body))
	server.router.ServeHTTP(w, req)
	err = json.Unmarshal(w.Body.Bytes(), &group)
	require.NoError(t, err)

	// Create study activity
	studyActivity, err := store.CreateStudyActivity(context.Background(), db.CreateStudyActivityParams{
		Name: "Test Activity",
		Url:  "http://example.com",
	})
	require.NoError(t, err)

	// Create test word
	partsJSON, err := json.Marshal(map[string]any{"type": "noun"})
	require.NoError(t, err)
	word, err := store.CreateWord(context.Background(), db.CreateWordParams{
		Malay:   "test",
		Jawi:    "تيس",
		English: "test",
		Parts:   partsJSON,
	})
	require.NoError(t, err)

	t.Run("Study Session CRUD", func(t *testing.T) {
		// Test CREATE study session
		createReq := createStudySessionRequest{
			GroupID:         pgtype.Int4{Int32: group.ID, Valid: true},
			StudyActivityID: pgtype.Int4{Int32: studyActivity.ID, Valid: true},
		}
		body, err := json.Marshal(createReq)
		require.NoError(t, err)

		w := httptest.NewRecorder()
		req, _ := http.NewRequest(http.MethodPost, "/api/study-sessions", bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusCreated, w.Code)

		var createdSession struct {
			ID             int32      `json:"id"`
			GroupID       pgtype.Int4 `json:"group_id"`
			StudyActivityID pgtype.Int4 `json:"study_activity_id"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &createdSession)
		require.NoError(t, err)
		require.Equal(t, group.ID, createdSession.GroupID.Int32)

		// Test LIST study sessions
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, "/api/study-sessions?limit=10&offset=0", nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		var listResponse []struct {
			ID             int32  `json:"id"`
			ActivityName   string `json:"activity_name"`
			GroupName     string `json:"group_name"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &listResponse)
		require.NoError(t, err)
		require.NotEmpty(t, listResponse)
		require.Equal(t, "Test Activity", listResponse[0].ActivityName)
		require.Equal(t, "Test Group", listResponse[0].GroupName)

		// Test CREATE review
		createReviewReq := createReviewRequest{
			WordID:  word.ID,
			Correct: true,
		}
		body, err = json.Marshal(createReviewReq)
		require.NoError(t, err)

		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodPost, fmt.Sprintf("/api/study-sessions/%d/reviews", createdSession.ID), bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusCreated, w.Code)

		// Test GET session reviews
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, fmt.Sprintf("/api/study-sessions/%d/reviews?limit=10&offset=0", createdSession.ID), nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		var reviews []struct {
			ID       int32      `json:"id"`
			WordID   pgtype.Int4 `json:"word_id"`
			Correct  bool       `json:"correct"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &reviews)
		require.NoError(t, err)
		require.NotEmpty(t, reviews)
		require.True(t, reviews[0].Correct)
	})

	t.Run("Error cases", func(t *testing.T) {
		// Test invalid study session creation
		invalidReq := map[string]interface{}{
			"group_id": "invalid",
		}
		body, err := json.Marshal(invalidReq)
		require.NoError(t, err)

		w := httptest.NewRecorder()
		req, _ := http.NewRequest(http.MethodPost, "/api/study-sessions", bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusBadRequest, w.Code)

		// Test invalid session ID for reviews
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, "/api/study-sessions/invalid/reviews", nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusBadRequest, w.Code)

		// Test invalid review creation
		invalidReviewReq := map[string]interface{}{
			"word_id": "invalid",
		}
		body, err = json.Marshal(invalidReviewReq)
		require.NoError(t, err)

		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodPost, "/api/study-sessions/1/reviews", bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusBadRequest, w.Code)
	})
}
