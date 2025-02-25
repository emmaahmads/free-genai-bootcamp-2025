-- name: GetStudyActivity :one
SELECT * FROM study_activities
WHERE id = $1 LIMIT 1;

-- name: ListStudyActivities :many
SELECT * FROM study_activities
ORDER BY id
LIMIT $1 OFFSET $2;

-- name: CreateStudyActivity :one
INSERT INTO study_activities (
    name,
    url
) VALUES (
    $1, $2
) RETURNING *;

-- name: UpdateStudyActivity :one
UPDATE study_activities
SET 
    name = $2,
    url = $3,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: DeleteStudyActivity :exec
DELETE FROM study_activities
WHERE id = $1;