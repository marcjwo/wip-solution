resource "random_id" "default" {
  byte_length = 8
}

data "archive_file" "default" {
  type        = "zip"
  source_dir  = "../../wip-cloud-function"
  output_path = "tmp/gcf-source.zip"
  excludes    = ["../../wip-cloud-functionprompt.txt"]
}

data "google_storage_project_service_account" "gcs_account" {
}

resource "google_storage_bucket" "gcf-source-bucket" {
  name                        = "${random_id.default.hex}-${var.project_id}-gcf-source-bucket"
  location                    = var.region
  uniform_bucket_level_access = true
  depends_on                  = [random_id.default]
}

resource "google_storage_bucket_object" "gcf-source-object" {
  name   = "gcf-source.zip"
  bucket = google_storage_bucket.gcf-source-bucket.name
  source = data.archive_file.default.output_path
}

resource "google_storage_bucket" "trigger-bucket" {
  name                        = "${random_id.default.hex}-${var.project_id}-data-trigger-bucket"
  location                    = var.region
  uniform_bucket_level_access = true
  depends_on                  = [random_id.default]
}

resource "google_storage_bucket" "prompt-bucket" {
  name                        = "${random_id.default.hex}-${var.project_id}-prompt-bucket"
  location                    = var.region
  uniform_bucket_level_access = true
  depends_on                  = [random_id.default]
}

resource "google_storage_bucket_object" "prompt-object" {
  name   = "prompt.txt"
  bucket = google_storage_bucket.prompt-bucket.name
  source = "../../wip-cloud-function/prompt.txt"
}

resource "google_project_iam_member" "gcs-pubsub-publishing" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"
}

resource "google_service_account" "account" {
  account_id   = "gcf-sa"
  display_name = "Service Account - used for both the cloud function and eventarc trigger"
}

resource "google_project_iam_member" "invoking" {
  project    = var.project_id
  role       = "roles/run.invoker"
  member     = "serviceAccount:${google_service_account.account.email}"
  depends_on = [google_project_iam_member.gcs-pubsub-publishing]
}

resource "google_project_iam_member" "event-receiving" {
  project    = var.project_id
  role       = "roles/eventarc.eventReceiver"
  member     = "serviceAccount:${google_service_account.account.email}"
  depends_on = [google_project_iam_member.invoking]
}

resource "google_project_iam_member" "artifactregistry-reader" {
  project    = var.project_id
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.account.email}"
  depends_on = [google_project_iam_member.event-receiving]
}

resource "google_cloudfunctions2_function" "default" {
  depends_on  = [google_project_iam_member.event-receiving, google_project_iam_member.artifactregistry-reader]
  project     = var.project_id
  name        = "document_extraction"
  location    = var.region
  description = "An event triggered python function to extract information from PDF and load those to BQ"
  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.storage.object.v1.finalized"
    retry_policy   = "RETRY_POLICY_RETRY"
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.trigger-bucket.name
    }
  }
  build_config {
    runtime     = "python312"
    entry_point = "hello_gcs"
    environment_variables = {
      SOURCE_HASH = data.archive_file.default.output_sha
    }
    source {
      storage_source {
        bucket = google_storage_bucket.gcf-source-bucket.name
        object = google_storage_bucket_object.gcf-source-object.name
      }
    }
  }
  service_config {
    max_instance_count               = 10
    min_instance_count               = 0
    available_memory                 = "4Gi"
    timeout_seconds                  = 60
    available_cpu                    = "4"
    max_instance_request_concurrency = 20
    environment_variables = {
      PROJECT_ID    = var.project_id
      DATASET_ID    = var.dataset_id
      TABLE_ID      = var.table_id
      PROMPT_BUCKET = google_storage_bucket.prompt-bucket.name
    }
  }
}

output "trigger-bucket" {
  value = google_storage_bucket.trigger-bucket.name
}
