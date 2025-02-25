-- Create words table
CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    malay TEXT NOT NULL,
    jawi TEXT NOT NULL,
    english TEXT NOT NULL,
    parts JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create groups table
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    words_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create word_groups join table
CREATE TABLE word_groups (
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (word_id, group_id)
);

-- Create study_activities table
CREATE TABLE study_activities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create study_sessions table
CREATE TABLE study_sessions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
    study_activity_id INTEGER REFERENCES study_activities(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create word_review_items table
CREATE TABLE word_review_items (
    id SERIAL PRIMARY KEY,
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    study_session_id INTEGER REFERENCES study_sessions(id) ON DELETE CASCADE,
    correct BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_words_malay ON words(malay);
CREATE INDEX idx_words_english ON words(english);
CREATE INDEX idx_groups_name ON groups(name);
CREATE INDEX idx_word_groups_word_id ON word_groups(word_id);
CREATE INDEX idx_word_groups_group_id ON word_groups(group_id);
CREATE INDEX idx_study_sessions_group_id ON study_sessions(group_id);
CREATE INDEX idx_study_sessions_activity_id ON study_sessions(study_activity_id);
CREATE INDEX idx_word_review_items_word_id ON word_review_items(word_id);
CREATE INDEX idx_word_review_items_session_id ON word_review_items(study_session_id);

-- Add triggers for updating words_count
CREATE OR REPLACE FUNCTION update_group_words_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE groups SET words_count = words_count + 1 WHERE id = NEW.group_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE groups SET words_count = words_count - 1 WHERE id = OLD.group_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER word_groups_after_insert
    AFTER INSERT ON word_groups
    FOR EACH ROW
    EXECUTE FUNCTION update_group_words_count();

CREATE TRIGGER word_groups_after_delete
    AFTER DELETE ON word_groups
    FOR EACH ROW
    EXECUTE FUNCTION update_group_words_count();
