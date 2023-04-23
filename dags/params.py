import os

# ENVIRONMENT VARIABLES
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# GOOGLE CLOUD VARIABLES
GCP_BUCKET_NAME = os.getenv("GCP_RAW_BUCKET")
PATH_TO_CREDENTIALS = os.getenv("PATH_TO_CREDENTIALS")

# OTHER PROJECT VARIABLES
REDIRECT_URI = "http://127.0.0.1:5000/callback/"
