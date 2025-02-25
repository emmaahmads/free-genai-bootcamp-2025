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
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/stretchr/testify/require"
)

func setupTestDB(t *testing.T) *pgxpool.Pool {
	dbURL := "postgresql://superumi:superspecial@localhost:5432/lang_portal?sslmode=disable"
	pool, err := pgxpool.New(context.Background(), dbURL)
	require.NoError(t, err)
	return pool
}

func createTestWord(t *testing.T, store *db.Queries) db.Word {
	partsJSON, err := json.Marshal(map[string]any{"type": "pronoun"})
	require.NoError(t, err)

	word, err := store.CreateWord(context.Background(), db.CreateWordParams{
		Malay:   "saya",
		Jawi:    "ساي",
		English: "I/me",
		Parts:   partsJSON,
	})
	require.NoError(t, err)
	return word
}

func setupTestServer(t *testing.T) (*Server, *db.Queries, func()) {
	pool := setupTestDB(t)
	server, err := NewServer(pool)
	require.NoError(t, err)
	store := db.New(pool)

	cleanup := func() {
		pool.Close()
	}

	return server, store, cleanup
}

func TestListWords(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	// Create test word
	word := createTestWord(t, store)
	defer store.DeleteWord(context.Background(), word.ID)

	// Create a test request
	req := httptest.NewRequest(http.MethodGet, "/api/words", nil)
	w := httptest.NewRecorder()

	// Serve the request
	server.router.ServeHTTP(w, req)

	// Check response
	require.Equal(t, http.StatusOK, w.Code)

	var response []db.Word
	err := json.Unmarshal(w.Body.Bytes(), &response)
	require.NoError(t, err)
	require.NotEmpty(t, response)
}

func TestGetWord(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	// Create test word
	word := createTestWord(t, store)
	defer store.DeleteWord(context.Background(), word.ID)

	// Test cases
	testCases := []struct {
		name          string
		wordID        string
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name:   "ExistingWord",
			wordID: fmt.Sprintf("%d", word.ID),
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)

				var response db.Word
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.Equal(t, word.ID, response.ID)
			},
		},
		{
			name:   "NonExistentWord",
			wordID: "999",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusNotFound, recorder.Code)
			},
		},
		{
			name:   "InvalidID",
			wordID: "invalid",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest, recorder.Code)
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create request
			url := fmt.Sprintf("/api/words/%s", tc.wordID)
			req := httptest.NewRequest(http.MethodGet, url, nil)
			w := httptest.NewRecorder()

			// Serve request
			server.router.ServeHTTP(w, req)

			// Check response
			tc.checkResponse(t, w)
		})
	}
}

func TestCreateWord(t *testing.T) {
	server, _, cleanup := setupTestServer(t)
	defer cleanup()

	// Test cases
	testCases := []struct {
		name          string
		request       createWordRequest
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name: "ValidWord",
			request: createWordRequest{
				Malay:   "rumah",
				Jawi:    "روماه",
				English: "house",
				Parts:   map[string]any{"type": "noun"},
			},
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusCreated, recorder.Code)

				var response db.Word
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.NotEmpty(t, response.ID)
				require.Equal(t, "rumah", response.Malay)
				require.Equal(t, "روماه", response.Jawi)
				require.Equal(t, "house", response.English)
			},
		},
		{
			name: "MissingFields",
			request: createWordRequest{
				Malay: "rumah",
				// Missing other required fields
			},
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest, recorder.Code)
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create request body
			body, err := json.Marshal(tc.request)
			require.NoError(t, err)

			// Create request
			req := httptest.NewRequest(http.MethodPost, "/api/words", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			// Serve request
			server.router.ServeHTTP(w, req)

			// Check response
			tc.checkResponse(t, w)
		})
	}
}

func TestUpdateWord(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	// Create test word
	word := createTestWord(t, store)
	defer store.DeleteWord(context.Background(), word.ID)

	// Test cases
	testCases := []struct {
		name          string
		wordID        string
		request       updateWordRequest
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name:   "ValidUpdate",
			wordID: fmt.Sprintf("%d", word.ID),
			request: updateWordRequest{
				Malay:   "saya",
				Jawi:    "ساي",
				English: "I/me/myself",
				Parts:   map[string]any{"type": "pronoun"},
			},
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)

				var response db.Word
				err := json.Unmarshal(recorder.Body.Bytes(), &response)
				require.NoError(t, err)
				require.Equal(t, word.ID, response.ID)
				require.Equal(t, "I/me/myself", response.English)
			},
		},
		{
			name:   "NonExistentWord",
			wordID: "999",
			request: updateWordRequest{
				Malay:   "test",
				Jawi:    "test",
				English: "test",
				Parts:   map[string]any{"type": "test"},
			},
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusNotFound, recorder.Code)
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create request body
			body, err := json.Marshal(tc.request)
			require.NoError(t, err)

			// Create request
			url := fmt.Sprintf("/api/words/%s", tc.wordID)
			req := httptest.NewRequest(http.MethodPut, url, bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			// Serve request
			server.router.ServeHTTP(w, req)

			// Check response
			tc.checkResponse(t, w)
		})
	}
}

func TestDeleteWord(t *testing.T) {
	server, store, cleanup := setupTestServer(t)
	defer cleanup()

	// Create test word
	word := createTestWord(t, store)

	// Test cases
	testCases := []struct {
		name          string
		wordID        string
		checkResponse func(t *testing.T, recorder *httptest.ResponseRecorder)
	}{
		{
			name:   "ValidDelete",
			wordID: fmt.Sprintf("%d", word.ID),
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusOK, recorder.Code)
			},
		},
		{
			name:   "NonExistentWord",
			wordID: "999",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusNotFound, recorder.Code)
			},
		},
		{
			name:   "InvalidID",
			wordID: "invalid",
			checkResponse: func(t *testing.T, recorder *httptest.ResponseRecorder) {
				require.Equal(t, http.StatusBadRequest, recorder.Code)
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create request
			url := fmt.Sprintf("/api/words/%s", tc.wordID)
			req := httptest.NewRequest(http.MethodDelete, url, nil)
			w := httptest.NewRecorder()

			// Serve request
			server.router.ServeHTTP(w, req)

			// Check response
			tc.checkResponse(t, w)
		})
	}
}
