CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    sign_up_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    points INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    date_posted TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    difficulty_level TEXT CHECK(difficulty_level IN ('Easy', 'Medium', 'Hard')),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS user_answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,  -- Determined at insertion
    attempt_number INTEGER NOT NULL CHECK(attempt_number BETWEEN 1 AND 3),
    date_posted TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, question_id, attempt_number),
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    answer_id INTEGER,
    user_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    date_posted TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (answer_id) REFERENCES user_answers(answer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
