-- Mock data for words table
INSERT INTO words (malay, jawi, english, parts) VALUES
('selamat datang', 'سلامت داتڠ', 'welcome', '{"noun": true, "phrase": true}'),
('terima kasih', 'تريما کاسيه', 'thank you', '{"phrase": true}'),
('apa khabar', 'اڤ خبر', 'how are you', '{"phrase": true, "question": true}'),
('saya', 'ساي', 'I', '{"pronoun": true}'),
('kamu', 'کامو', 'you', '{"pronoun": true}'),
('dia', 'دي', 'he/she', '{"pronoun": true}'),
('makan', 'ماکن', 'eat', '{"verb": true}'),
('tidur', 'تيدور', 'sleep', '{"verb": true}'),
('belajar', 'بلاجر', 'study', '{"verb": true}'),
('rumah', 'روماه', 'house', '{"noun": true}'),
('sekolah', 'سکوله', 'school', '{"noun": true}'),
('kereta', 'کريتا', 'car', '{"noun": true}'),
('cepat', 'چڤت', 'fast', '{"adjective": true}'),
('lambat', 'لمبت', 'slow', '{"adjective": true}'),
('cantik', 'چنتيق', 'beautiful', '{"adjective": true}'),
('air', 'اءير', 'water', '{"noun": true}'),
('nasi', 'ناسي', 'rice', '{"noun": true}'),
('kucing', 'کوچيڠ', 'cat', '{"noun": true}'),
('anjing', 'انجيڠ', 'dog', '{"noun": true}'),
('burung', 'بوروڠ', 'bird', '{"noun": true}');

-- Mock data for groups table
INSERT INTO groups (name) VALUES
('Basic Greetings'),
('Common Phrases'),
('Pronouns'),
('Verbs'),
('Nouns'),
('Adjectives'),
('Animals'),
('Food and Drinks');

-- Mock data for word_groups join table
-- Basic Greetings
INSERT INTO word_groups (word_id, group_id) VALUES
(1, 1), -- selamat datang
(2, 1), -- terima kasih
(3, 1); -- apa khabar

-- Common Phrases
INSERT INTO word_groups (word_id, group_id) VALUES
(1, 2), -- selamat datang
(2, 2), -- terima kasih
(3, 2); -- apa khabar

-- Pronouns
INSERT INTO word_groups (word_id, group_id) VALUES
(4, 3), -- saya
(5, 3), -- kamu
(6, 3); -- dia

-- Verbs
INSERT INTO word_groups (word_id, group_id) VALUES
(7, 4), -- makan
(8, 4), -- tidur
(9, 4); -- belajar

-- Nouns
INSERT INTO word_groups (word_id, group_id) VALUES
(10, 5), -- rumah
(11, 5), -- sekolah
(12, 5); -- kereta

-- Adjectives
INSERT INTO word_groups (word_id, group_id) VALUES
(13, 6), -- cepat
(14, 6), -- lambat
(15, 6); -- cantik

-- Animals
INSERT INTO word_groups (word_id, group_id) VALUES
(18, 7), -- kucing
(19, 7), -- anjing
(20, 7); -- burung

-- Food and Drinks
INSERT INTO word_groups (word_id, group_id) VALUES
(16, 8), -- air
(17, 8); -- nasi

-- Mock data for study_activities table
INSERT INTO study_activities (name, url) VALUES
('Flashcards', '/activities/flashcards'),
('Multiple Choice Quiz', '/activities/quiz'),
('Spelling Practice', '/activities/spelling'),
('Listening Exercise', '/activities/listening'),
('Translation Challenge', '/activities/translation');

-- Mock data for study_sessions
-- Create study sessions for different groups and activities
INSERT INTO study_sessions (group_id, study_activity_id) VALUES
(1, 1), -- Basic Greetings - Flashcards
(2, 2), -- Common Phrases - Multiple Choice Quiz
(3, 3), -- Pronouns - Spelling Practice
(4, 4), -- Verbs - Listening Exercise
(5, 5), -- Nouns - Translation Challenge
(6, 1), -- Adjectives - Flashcards
(7, 2), -- Animals - Multiple Choice Quiz
(8, 3); -- Food and Drinks - Spelling Practice

-- Mock data for word_review_items
-- For Basic Greetings - Flashcards session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(1, 1, true),  -- selamat datang - correct
(2, 1, true),  -- terima kasih - correct
(3, 1, false); -- apa khabar - incorrect

-- For Common Phrases - Multiple Choice Quiz session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(1, 2, true),  -- selamat datang - correct
(2, 2, true),  -- terima kasih - correct
(3, 2, true);  -- apa khabar - correct

-- For Pronouns - Spelling Practice session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(4, 3, true),  -- saya - correct
(5, 3, false), -- kamu - incorrect
(6, 3, true);  -- dia - correct

-- For Verbs - Listening Exercise session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(7, 4, true),  -- makan - correct
(8, 4, false), -- tidur - incorrect
(9, 4, true);  -- belajar - correct

-- For Nouns - Translation Challenge session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(10, 5, true), -- rumah - correct
(11, 5, true), -- sekolah - correct
(12, 5, false); -- kereta - incorrect

-- For Adjectives - Flashcards session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(13, 6, true), -- cepat - correct
(14, 6, true), -- lambat - correct
(15, 6, true); -- cantik - correct

-- For Animals - Multiple Choice Quiz session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(18, 7, true), -- kucing - correct
(19, 7, false), -- anjing - incorrect
(20, 7, true); -- burung - correct

-- For Food and Drinks - Spelling Practice session
INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES
(16, 8, true), -- air - correct
(17, 8, true); -- nasi - correct
