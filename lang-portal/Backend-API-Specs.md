# Backend API Specification

This document outlines the API endpoints for the Language Learning Portal backend. All endpoints return JSON responses.

## Base URL
```
/api
```

## Authentication
All endpoints require authentication (to be implemented)

## Endpoints

### Dashboard

#### GET /api/dashboard/last_study_session
Returns information about the user's last study session.

**Response**
```json
{
  "activity_name": "string",
  "group_name": "string",
  "timestamp": "ISO8601 string",
  "stats": {
    "correct": "integer",
    "wrong": "integer"
  },
  "group_id": "integer"
}
```

#### GET /api/dashboard/study_progress
Returns the user's overall study progress.

**Response**
```json
{
  "total_words_studied": "integer",
  "total_available_words": "integer",
  "mastery_percentage": "float"
}
```

#### GET /api/dashboard/quick_stats
Returns quick statistics about the user's learning progress.

**Response**
```json
{
  "success_rate": "float",
  "total_study_sessions": "integer",
  "total_active_groups": "integer",
  "study_streak_days": "integer"
}
```

### Study Activities

#### GET /api/study_activities
Returns a list of available study activities.

**Response**
```json
{
  "activities": [
    {
      "id": "integer",
      "name": "string",
      "thumbnail_url": "string",
      "description": "string"
    }
  ]
}
```

#### GET /api/study_activities/:id
Returns details about a specific study activity.

**Parameters**
- id: Activity ID (integer)

**Response**
```json
{
  "id": "integer",
  "name": "string",
  "thumbnail_url": "string",
  "description": "string"
}
```

#### GET /api/study_activities/:id/study_sessions
Returns a paginated list of study sessions for a specific activity.

**Parameters**
- id: Activity ID (integer)
- page: Page number (integer, optional)
- per_page: Items per page (integer, optional)

**Response**
```json
{
  "study_sessions": [
    {
      "id": "integer",
      "activity_name": "string",
      "group_name": "string",
      "start_time": "ISO8601 string",
      "end_time": "ISO8601 string",
      "review_items_count": "integer"
    }
  ],
  "pagination": {
    "current_page": "integer",
    "total_pages": "integer",
    "total_items": "integer"
  }
}
```

#### POST /api/study_activities
Creates a new study session.

**Request Body**
```json
{
  "activity_id": "integer",
  "group_id": "integer"
}
```

**Response**
```json
{
  "session_id": "integer",
  "activity_url": "string"
}
```

### Words

#### GET /api/words
Returns a paginated list of words.

**Parameters**
- page: Page number (integer, optional, default=1)
- per_page: Items per page (integer, optional, default=100)

**Response**
```json
{
  "words": [
    {
      "id": "integer",
      "malay": "string",
      "jawi": "string",
      "english": "string",
      "correct_count": "integer",
      "wrong_count": "integer"
    }
  ],
  "pagination": {
    "current_page": "integer",
    "total_pages": "integer",
    "total_items": "integer"
  }
}
```

#### GET /api/words/:id
Returns details about a specific word.

**Parameters**
- id: Word ID (integer)

**Response**
```json
{
  "id": "integer",
  "malay": "string",
  "jawi": "string",
  "english": "string",
  "stats": {
    "correct_count": "integer",
    "wrong_count": "integer"
  },
  "groups": [
    {
      "id": "integer",
      "name": "string"
    }
  ]
}
```

### Groups

#### GET /api/groups
Returns a paginated list of word groups.

**Parameters**
- page: Page number (integer, optional)
- per_page: Items per page (integer, optional)

**Response**
```json
{
  "groups": [
    {
      "id": "integer",
      "name": "string",
      "word_count": "integer"
    }
  ],
  "pagination": {
    "current_page": "integer",
    "total_pages": "integer",
    "total_items": "integer"
  }
}
```

#### GET /api/groups/:id
Returns details about a specific group.

**Parameters**
- id: Group ID (integer)

**Response**
```json
{
  "id": "integer",
  "name": "string",
  "word_count": "integer",
  "words": [
    {
      "id": "integer",
      "malay": "string",
      "jawi": "string",
      "english": "string"
    }
  ]
}
```

## Error Responses
All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "string",
  "message": "string"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```
