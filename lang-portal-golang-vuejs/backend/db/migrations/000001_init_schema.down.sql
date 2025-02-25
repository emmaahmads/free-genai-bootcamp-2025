-- Drop triggers first
DROP TRIGGER IF EXISTS word_groups_after_insert ON word_groups;
DROP TRIGGER IF EXISTS word_groups_after_delete ON word_groups;
DROP FUNCTION IF EXISTS update_group_words_count();

-- Drop tables in reverse order of creation (respecting foreign key constraints)
DROP TABLE IF EXISTS word_review_items;
DROP TABLE IF EXISTS study_sessions;
DROP TABLE IF EXISTS study_activities;
DROP TABLE IF EXISTS word_groups;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS words;
