#create a bucket to store raw data files
direnv allow & direnv reload
gsutil mb -b on -l EUROPE-WEST3 gs://$GCP_RAW_BUCKET/
