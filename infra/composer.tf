#Activate cloud composer API on project
resource "google_project_service" "composer_api" {
  provider           = google
  project            = var.project
  service            = "composer.googleapis.com"
  disable_on_destroy = false
}

#Create a service account
resource "google_service_account" "composer_service_account" {
  provider     = google
  account_id   = "composer-service-account"
  display_name = "Composer Service Account"
}

#Add all the roles needed
resource "google_project_iam_member" "composer_service_account" {
  provider = google
  project  = var.project
  member   = format("serviceAccount:%s", google_service_account.composer_service_account.email)
  // Role for Public IP environments
  role = "roles/composer.worker"
}

resource "google_service_account_iam_member" "composer_service_account" {
  provider           = google
  service_account_id = google_service_account.composer_service_account.name
  role               = "roles/composer.ServiceAgentV2Ext"
  member             = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}



resource "google_composer_environment" "tracks" {
  provider = google
  name     = "tracks"
  region   = var.region

  config {
    software_config {
      image_version = "composer-2.1.14-airflow-2.5.1"
    }
    node_config {
      service_account = google_service_account.composer_service_account.email
    }
  }

}
