package api

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestGroupEndpoints(t *testing.T) {
	server, _, cleanup := setupTestServer(t)
	defer cleanup()

	// Clean up any existing data
	_, err := server.pool.Exec(context.Background(), `
		TRUNCATE word_groups CASCADE;
		TRUNCATE study_sessions CASCADE;
		TRUNCATE groups CASCADE;
	`)
	require.NoError(t, err)

	t.Run("CRUD operations", func(t *testing.T) {
		// Test CREATE
		createReq := createGroupRequest{
			Name: "Test Group",
		}
		body, err := json.Marshal(createReq)
		require.NoError(t, err)

		w := httptest.NewRecorder()
		req, _ := http.NewRequest(http.MethodPost, "/api/groups", bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusCreated, w.Code)

		var createdGroup struct {
			ID   int32  `json:"id"`
			Name string `json:"name"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &createdGroup)
		require.NoError(t, err)
		require.Equal(t, createReq.Name, createdGroup.Name)

		// Test GET single group
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, fmt.Sprintf("/api/groups/%d", createdGroup.ID), nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		var fetchedGroup struct {
			ID   int32  `json:"id"`
			Name string `json:"name"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &fetchedGroup)
		require.NoError(t, err)
		require.Equal(t, createdGroup.ID, fetchedGroup.ID)
		require.Equal(t, createdGroup.Name, fetchedGroup.Name)

		// Test LIST groups
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, "/api/groups", nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		var groups []struct {
			ID   int32  `json:"id"`
			Name string `json:"name"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &groups)
		require.NoError(t, err)
		require.NotEmpty(t, groups)
		found := false
		for _, g := range groups {
			if g.ID == createdGroup.ID {
				found = true
				require.Equal(t, createdGroup.Name, g.Name)
				break
			}
		}
		require.True(t, found)

		// Test UPDATE
		updateReq := updateGroupRequest{
			Name: "Updated Test Group",
		}
		body, err = json.Marshal(updateReq)
		require.NoError(t, err)

		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodPut, fmt.Sprintf("/api/groups/%d", createdGroup.ID), bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		var updatedGroup struct {
			ID   int32  `json:"id"`
			Name string `json:"name"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &updatedGroup)
		require.NoError(t, err)
		require.Equal(t, createdGroup.ID, updatedGroup.ID)
		require.Equal(t, updateReq.Name, updatedGroup.Name)

		// Test DELETE
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodDelete, fmt.Sprintf("/api/groups/%d", createdGroup.ID), nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		// Verify deletion
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, fmt.Sprintf("/api/groups/%d", createdGroup.ID), nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusNotFound, w.Code)
	})

	t.Run("Get group words", func(t *testing.T) {
		// Create a test group
		group := createGroupRequest{
			Name: "Word Group",
		}
		body, err := json.Marshal(group)
		require.NoError(t, err)

		w := httptest.NewRecorder()
		req, _ := http.NewRequest(http.MethodPost, "/api/groups", bytes.NewReader(body))
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusCreated, w.Code)

		var createdGroup struct {
			ID int32 `json:"id"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &createdGroup)
		require.NoError(t, err)

		// Test get words for the group
		w = httptest.NewRecorder()
		req, _ = http.NewRequest(http.MethodGet, fmt.Sprintf("/api/groups/%d/words", createdGroup.ID), nil)
		server.router.ServeHTTP(w, req)
		require.Equal(t, http.StatusOK, w.Code)

		var words []struct {
			ID      int32          `json:"id"`
			Malay   string        `json:"malay"`
			Jawi    string        `json:"jawi"`
			English string        `json:"english"`
			Parts   map[string]any `json:"parts"`
		}
		err = json.Unmarshal(w.Body.Bytes(), &words)
		require.NoError(t, err)
		// Initially the group should have no words
		require.Empty(t, words)
	})
}
