CREATE TABLE IF NOT EXISTS tracks(
  "id" TEXT PRIMARY KEY,
  "danceability" FLOAT,
  "energy" FLOAT,
  "key" INTEGER,
  "loudness" FLOAT,
  "mode" INTEGER,
  "speechiness" FLOAT,
  "acousticness" FLOAT,
  "instrumentalness" FLOAT,
  "liveness" FLOAT,
  "valence" FLOAT,
  "tempo" FLOAT,
  "duration_ms" INTEGER,
  "time_signature" INTEGER
)
