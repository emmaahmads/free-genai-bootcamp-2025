# Backend API Specification

This document outlines the API endpoints for the Language Learning Portal backend. All endpoints return JSON responses.

## Base URL
```
/api
```

## Endpoints

### Dashboard

#### GET /api/dashboard/last_study_session
Returns information about the user's last study session.

**Response**
```json
{
  "id": 123,
  "group_id": 456,
  "created_at": "2025-02-08T17:20:23-05:00",
  "study_activity_id": 789,
  "group_name": "Basic Greetings"
}
```

#### GET /api/dashboard/study_progress
Returns the user's overall study progress.

**Response**
```json
{
  "total_words_studied": 3,
  "total_available_words": 124
}
```

#### GET /api/dashboard/quick_stats
Returns quick statistics about the user's learning progress.

**Response**
```json
{
  "success_rate": 80.0,
  "total_study_sessions": 4,
  "total_active_groups": 3,
  "study_streak_days": 4
}
```

### Study Activities

#### GET /api/study_activities
Returns a list of available study activities.

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Vocabulary Quiz",
      "thumbnail_url": "https://example.com/thumbnail.jpg",
      "description": "Practice your vocabulary with flashcards"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 100
  }
}
```

#### GET /api/study_activities/:id
Returns details about a specific study activity.

**Response**
```json
{
  "id": 1,
  "name": "Vocabulary Quiz",
  "thumbnail_url": "https://example.com/thumbnail.jpg",
  "description": "Practice your vocabulary with flashcards"
}
```

#### GET /api/study_activities/:id/study_sessions
Returns a paginated list of study sessions for a specific activity.

**Response**
```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 20
  }
}
```

#### POST /api/study_activities
Creates a new study session. The response includes the activity URL which should be opened in a new tab.

**Request Parameters**
- group_id: integer
- study_activity_id: integer

**Response**
```json
{
  "id": 124,
  "group_id": 123,
  "activity_url": "https://example.com/activities/vocabulary-quiz",
  "study_session_id": 456
}
```

### Study Sessions

#### GET /api/study_sessions
Returns a paginated list of study sessions.

**Response**
```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 100
  }
}
```

#### GET /api/study_sessions/:id
Returns details about a specific study session.

**Response**
```json
{
  "id": 123,
  "activity_name": "Vocabulary Quiz",
  "group_name": "Basic Greetings",
  "start_time": "2025-02-08T17:20:23-05:00",
  "end_time": "2025-02-08T17:30:23-05:00",
  "review_items_count": 20
}
```

#### GET /api/study_sessions/:id/words
Returns a paginated list of words for a specific study session.

**Response**
```json
{
  "items": [
    {
      "malay": "Selamat pagi",
      "jawi": "سلامت ڤاݢي",
      "english": "good morning",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```

### Words

#### GET /api/words
Returns a paginated list of words.

**Response**
```json
{
  "items": [
    {
      "malay": "Selamat pagi",
      "jawi": "سلامت ڤاݢي",
      "english": "good morning",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 500,
    "items_per_page": 100
  }
}
```

#### GET /api/words/:id
Returns details about a specific word.

**Response**
```json
{
  "malay": "Selamat pagi",
  "jawi": "سلامت ڤاݢي",
  "english": "good morning",
  "stats": {
    "correct_count": 5,
    "wrong_count": 2
  },
  "groups": [
    {
      "id": 1,
      "name": "Basic Greetings"
    }
  ]
}
```

### Groups

#### GET /api/groups
Returns a paginated list of word groups.

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Basic Greetings",
      "word_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 10,
    "items_per_page": 100
  }
}
```

#### GET /api/groups/:id
Returns details about a specific group.

**Response**
```json
{
  "id": 1,
  "name": "Basic Greetings",
  "stats": {
    "total_word_count": 20
  }
}
```

#### GET /api/groups/:id/words
Returns a paginated list of words in a specific group.

**Response**
```json
{
  "items": [
    {
      "malay": "Selamat pagi",
      "jawi": "سلامت ڤاݢي",
      "english": "good morning",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```

#### GET /api/groups/:id/study_sessions
Returns a paginated list of study sessions for a specific group.

**Response**
```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 5,
    "items_per_page": 100
  }
}
```

### Additional Endpoints

#### POST /api/reset_history
Resets all study history.

**Response**
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```

#### POST /api/full_reset
Performs a full system reset.

**Response**
```json
{
  "success": true,
  "message": "System has been fully reset"
}
```

#### POST /api/study_sessions/:id/words/:word_id/review
Submits a word review for a study session.

**Request Parameters**
- id (study_session_id): integer
- word_id: integer
- correct: boolean

**Request Payload**
```json
{
  "correct": true
}
```

**Response**
```json
{
  "success": true,
  "word_id": 1,
  "study_session_id": 123,
  "correct": true,
  "created_at": "2025-02-08T17:33:07-05:00"
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

# Database Schema

words — Stores individual Malay vocabulary words.
- `id` (Primary Key): Unique identifier for each word
- `malay` (String, Required): The word written in Malay
- `jawi` (String, Required): The word written in Jawi script
- `english` (String, Required): English translation of the word
- `parts` (JSON, Required): Word components stored in JSON format

groups — Manages collections of words.
- `id` (Primary Key): Unique identifier for each group
- `name` (String, Required): Name of the group
- `words_count` (Integer, Default: 0): Counter cache for the number of words in the group

word_groups — join-table enabling many-to-many relationship between words and groups.
- `word_id` (Foreign Key): References words.id
- `group_id` (Foreign Key): References groups.id

study_activities — Defines different types of study activities available.
- `id` (Primary Key): Unique identifier for each activity
- `name` (String, Required): Name of the activity (e.g., "Flashcards", "Quiz")
- `url` (String, Required): The full URL of the study activity

study_sessions — Records individual study sessions.
- `id` (Primary Key): Unique identifier for each session
- `group_id` (Foreign Key): References groups.id
- `study_activity_id` (Foreign Key): References study_activities.id
- `created_at` (Timestamp, Default: Current Time): When the session was created

word_review_items — Tracks individual word reviews within study sessions.
- `id` (Primary Key): Unique identifier for each review
- `word_id` (Foreign Key): References words.id
- `study_session_id` (Foreign Key): References study_sessions.id
- `correct` (Boolean, Required): Whether the answer was correct
- `created_at` (Timestamp, Default: Current Time): When the review occurred

Relationships:
- word belongs to groups through word_groups
- group belongs to words through word_groups
- session belongs to a group
- session belongs to a study_activity
- session has many word_review_items
- word_review_item belongs to a study_session
- word_review_item belongs to a word

Design Notes:
- All tables use auto-incrementing primary keys
- Timestamps are automatically set on creation where applicable
- Foreign key constraints maintain referential integrity
- JSON storage for word parts allows flexible component storage
- Counter cache on groups.words_count optimizes word counting queries