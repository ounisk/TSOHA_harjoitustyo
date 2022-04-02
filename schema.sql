CREATE TABLE allusers (
    id SERIAL PRIMARY KEY,
    username TEXT,
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
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES allusers
);
CREATE TABLE allmessages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES allusers,
    sent_at TIMESTAMP
);
CREATE TABLE topics_private (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES allusers
);
