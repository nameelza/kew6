-- We have 2 tables:
CREATE TABLE songs (
    id INTEGER,
    name TEXT,
    artist_id INTEGER,
    danceability REAL,
    energy REAL,
    key INTEGER,
    loudness REAL,
    speechiness REAL,
    valence REAL,
    tempo REAL,
    duration_ms INTEGER
);
CREATE TABLE artists (
    id INTEGER,
    name TEXT
);

-- Output: list of all the song names and corresponding artist names from different tables

SELECT songs.name, artists.name FROM songs, artists WHERE songs.artist_id = artists.id;
