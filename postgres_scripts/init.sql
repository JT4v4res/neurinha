DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS session_users;
DROP TABLE IF EXISTS chat_history;
DROP TABLE IF EXISTS elegant_messages;

CREATE TABLE elegant_messages (
    id SERIAL PRIMARY KEY,
    message_author TEXT,
    message TEXT,
    created_at TIMESTAMPTZ default current_timestamp
);

CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    session_id uuid,
    message JSONB,
    created_at TIMESTAMPTZ default current_timestamp
);

CREATE TABLE sessions (
	id SERIAL PRIMARY KEY,
	session_id UUID NOT NULL UNIQUE,
	is_active BOOL,
	created_at TIMESTAMPTZ DEFAULT current_timestamp
);

CREATE TABLE session_users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	user_token UUID,
	session_id UUID NOT NULL,
	validation_number INT,
	secret_phrase TEXT,
	FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);
