resource "google_storage_bucket" "static" {
  name     = "spotify-custom-recommendation-raw-data"
  location = "EU"
}
