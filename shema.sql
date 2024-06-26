CREATE TABLE IF NOT EXISTS Posts (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
body TEXT NOT NULL,
user_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Comments (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
email TEXT NOT NULL,
body TEXT NOT NULL
);

ALTER TABLE Comments ADD post_id BIGINT REFERENCES Posts (id);