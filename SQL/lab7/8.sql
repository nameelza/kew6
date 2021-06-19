SELECT name FROM songs WHERE artist_id IN (SELECT id FROM artists WHERE name = "Post Malone");


SELECT name FROM songs, artists WHERE songs.name = artists.name;