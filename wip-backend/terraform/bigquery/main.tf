resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset_id
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "table" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = var.table_id
  schema              = file("${path.module}/bq_schema.json")
  deletion_protection = false
}
