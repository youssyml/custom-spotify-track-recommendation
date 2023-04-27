# Custom Spotify Track Recommendation

The goal of this project is to upskill myself on key technologies for a Machine Learning Engineer (Airflow, Terraform, Kubernetes) while building a custom track exploration and recommendation engine based on my Spotify profile.

## Repository structure
- training-data-app: app to fetch training data from user spotify profile
- infra: code to create the project's infrastructure on Google Cloud using Terraform and shell scripts
- dags: Airflow DAG code to fetch and process spotify track data
- helm: Docker image and configuration for deploying airflow using helm on GKE
