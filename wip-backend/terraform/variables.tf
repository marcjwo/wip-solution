# Required variables
variable "project_id" {
  type        = string
  description = "Google Cloud Project ID "
}

# Variables with default values
variable "region" {
  type        = string
  description = "Google Cloud Region"
  default     = "europe-west3"
}

# Variables to set
variable "dataset_id" {
  type        = string
  description = "Name of the dataset for the tables containing data extracts"
}

variable "table_id" {
  type        = string
  description = "Name of the table to store the data extracts in"
}
