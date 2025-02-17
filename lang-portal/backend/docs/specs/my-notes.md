Based on the Backend API Specifications, here's a summary of all the APIs to be implemented:

## Dashboard APIs
GET /api/dashboard/last_study_session - Get user's last study session info
GET /api/dashboard/study_progress - Get overall study progress
GET /api/dashboard/quick_stats - Get learning progress statistics

## Study Activities APIs
GET /api/study_activities - List all available study activities
GET /api/study_activities/:id - Get specific activity details
GET /api/study_activities/:id/study_sessions - Get paginated study sessions for an activity
POST /api/study_activities - Create a new study session

## Study Sessions APIs
GET /api/study_sessions - Get paginated list of study sessions
GET /api/study_sessions/:id - Get specific study session details
GET /api/study_sessions/:id/words - Get paginated list of words for a study session

## Words APIs
GET /api/words - Get paginated list of words
GET /api/words/:id - Get specific word details

## Additional Endpoints
POST /api/reset_history - Reset study history
POST /api/full_reset - Full system reset
POST /api/study_sessions/:id/words/:word_id/review - Submit a word review for a study session

## Groups APIs
GET /api/groups - Get paginated list of word groups
GET /api/groups/:id - Get specific group details
All endpoints:

Use /api as the base URL
Return JSON responses
Include standard error responses (400, 401, 404, 500)
Support pagination where applicable