-- name: GetWord :one
SELECT * FROM words
WHERE id = $1 LIMIT 1;

-- name: ListWords :many
SELECT * FROM words
WHERE 
    CASE 
        WHEN sqlc.narg('search_query')::text != '' THEN 
            malay ILIKE concat('%', sqlc.narg('search_query')::text, '%') OR
            english ILIKE concat('%', sqlc.narg('search_query')::text, '%')
        ELSE true
    END
ORDER BY id
LIMIT sqlc.arg('limit')
OFFSET sqlc.arg('offset');

-- name: CreateWord :one
INSERT INTO words (
    malay,
    jawi,
    english,
    parts
) VALUES (
    $1, $2, $3, $4
) RETURNING *;

-- name: UpdateWord :one
UPDATE words
SET 
    malay = COALESCE($2, malay),
    jawi = COALESCE($3, jawi),
    english = COALESCE($4, english),
    parts = COALESCE($5, parts),
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: DeleteWord :exec
DELETE FROM words
WHERE id = $1;

-- name: SearchWords :many
SELECT * FROM words
WHERE 
    malay ILIKE $1 OR 
    english ILIKE $1
ORDER BY id
LIMIT $2 OFFSET $3;

-- name: GetWordsByGroup :many
SELECT w.* FROM words w
JOIN word_groups wg ON w.id = wg.word_id
WHERE wg.group_id = $1
ORDER BY w.id
LIMIT $2 OFFSET $3;