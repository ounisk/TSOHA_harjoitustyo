CREATE TABLE allusers (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN DEFAULT false
);
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    visible BOOLEAN DEFAULT TRUE
);
CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    thread TEXT,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    user_id INTEGER REFERENCES allusers ON DELETE CASCADE
);
CREATE TABLE allmessages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    user_id INTEGER REFERENCES allusers ON DELETE CASCADE,
    sent_at TIMESTAMP
);
CREATE TABLE topics_private (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    user_id INTEGER REFERENCES allusers ON DELETE CASCADE
);
