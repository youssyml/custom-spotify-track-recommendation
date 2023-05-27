DROP TABLE IF EXISTS tracks_genres;
CREATE TABLE IF NOT EXISTS tracks_genres(
  "track_id" TEXT,
  "genre_id" INTEGER,
  CONSTRAINT "track_genre_pk" PRIMARY KEY ("track_id","genre_id")
)
