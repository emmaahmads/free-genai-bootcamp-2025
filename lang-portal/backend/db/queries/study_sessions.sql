-- name: GetStudySession :one
SELECT * FROM study_sessions
WHERE id = $1 LIMIT 1;

-- name: ListStudySessions :many
SELECT 
    ss.*,
    sa.name as activity_name,
    g.name as group_name,
    COUNT(wri.id) as review_items_count
FROM study_sessions ss
JOIN study_activities sa ON ss.study_activity_id = sa.id
JOIN groups g ON ss.group_id = g.id
LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
GROUP BY ss.id, sa.name, g.name
ORDER BY ss.created_at DESC
LIMIT $1 OFFSET $2;

-- name: CreateStudySession :one
INSERT INTO study_sessions (
    group_id,
    study_activity_id
) VALUES (
    $1, $2
) RETURNING *;

-- name: GetLastStudySession :one
SELECT 
    ss.*,
    sa.name as activity_name,
    g.name as group_name,
    COUNT(wri.id) as review_items_count
FROM study_sessions ss
JOIN study_activities sa ON ss.study_activity_id = sa.id
JOIN groups g ON ss.group_id = g.id
LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
GROUP BY ss.id, sa.name, g.name
ORDER BY ss.created_at DESC
LIMIT 1;

-- name: CreateWordReview :one
INSERT INTO word_review_items (
    word_id,
    study_session_id,
    correct
) VALUES (
    $1, $2, $3
) RETURNING *;

-- name: GetSessionReviews :many
SELECT 
    wri.*,
    w.malay,
    w.jawi,
    w.english
FROM word_review_items wri
JOIN words w ON wri.word_id = w.id
WHERE wri.study_session_id = $1
ORDER BY wri.created_at
LIMIT $2 OFFSET $3;

-- name: GetStudyProgress :one
SELECT 
    COUNT(DISTINCT word_id) as total_words_studied,
    (SELECT COUNT(*) FROM words) as total_available_words
FROM word_review_items;

-- name: GetQuickStats :one
WITH stats AS (
    SELECT 
        COUNT(*) as total_reviews,
        SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_reviews
    FROM word_review_items
)
SELECT 
    CASE 
        WHEN total_reviews > 0 THEN (correct_reviews::float / total_reviews::float) * 100 
        ELSE 0 
    END as success_rate,
    (SELECT COUNT(DISTINCT id) FROM study_sessions) as total_study_sessions,
    (SELECT COUNT(*) FROM groups WHERE words_count > 0) as total_active_groups,
    (SELECT COUNT(DISTINCT DATE(created_at))
     FROM study_sessions 
     WHERE created_at >= CURRENT_DATE - INTERVAL '30 days') as study_streak_days
FROM stats;
