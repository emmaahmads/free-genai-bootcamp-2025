-- name: GetGroup :one
SELECT * FROM groups
WHERE id = $1 LIMIT 1;

-- name: ListGroups :many
SELECT * FROM groups
ORDER BY id
LIMIT $1 OFFSET $2;

-- name: CreateGroup :one
INSERT INTO groups (
    name
) VALUES (
    $1
) RETURNING *;

-- name: UpdateGroup :one
UPDATE groups
SET 
    name = $2,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: DeleteGroup :exec
WITH deleted AS (
    SELECT id FROM groups WHERE id = $1
)
DELETE FROM groups
WHERE id = $1 AND EXISTS (SELECT 1 FROM deleted);

-- name: AddWordToGroup :exec
INSERT INTO word_groups (
    word_id,
    group_id
) VALUES (
    $1, $2
);

-- name: RemoveWordFromGroup :exec
DELETE FROM word_groups
WHERE word_id = $1 AND group_id = $2;

-- name: GetGroupsByWord :many
SELECT g.* FROM groups g
JOIN word_groups wg ON g.id = wg.group_id
WHERE wg.word_id = $1
ORDER BY g.id
LIMIT $2 OFFSET $3;