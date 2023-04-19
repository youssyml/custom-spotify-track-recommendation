import os

# ENVIRONMENT VARIABLES
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# GOOGLE CLOUD VARIABLES
GCP_BUCKET_NAME = os.getenv("GCP_RAW_BUCKET")

# OTHER PROJECT VARIABLES
REDIRECT_URI = "http://127.0.0.1:5000/callback/"

# SPOTIFY VARIABLES
DISLIKES_PLAYLIST_ID = "3XETYosk1OaNkmUoBzXnDl"
LIKES_PLAYLIST_ID = "39X76QUygTqHKcZ4kPAZBR"
