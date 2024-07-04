# WIP Solution Backend

## Overview

This Terraform configuration creates all the necessary infrastructure artifacts to deploy the WIP solution on Google Cloud Platform (GCP), facilitating interaction with the Gemini Flash model of Vertex AI.

## Prerequisites

- Terraform installed on your machine
- Access to a GCP account with permission to create and manage resources
- A GCP project to deploy resources

## Config and deployment

From the `./wip_backend` directory do the following.

### Create the required BQ schema

Navigate to the `terraform/bigquery` directory (ie. `cd terraform/bigquery`). The folder contains a `sample_bq_schema.json` file for reference. Create a new `bq_schema.json` file (ie. `touch bq_schema.json`) and define the schema following [json schema requirements](https://cloud.google.com/bigquery/docs/schemas#creating_a_JSON_schema_file). The schema that is defined here derives from the instructions/prompt defined for the cloud function on what fields to extract.

### Set required variables

cd back to `./wip_backend` directory first. Then do the following.

```bash
cd terraform
export TF_VAR_project_id=<YOUR_PROJECT_ID>
export TF_VAR_dataset_id=<YOUR_DATASET_ID>
export TF_VAR_table_id=<YOUR_TABLE_ID>
export TF_VAR_region=<YOUR_REGION> (The default region is europe-west3, only set this if you want to deploy to a different region)
```

### Deploy infrastructure using terraform

Ensure you are in the `./wip_backend/terraform` directory. Then do the following.

```bash
terraform init
terraform plan
terraform apply
```

## Resources created

- BigQuery dataset
- BigQuery table
- Trigger GCS bucket
- Prompt GCS bucket
- Cloud Function 2nd Gen, triggered by changes in trigger bucket

## Cleaning Up

To remove all resources created by this Terraform configuration, run:

```bash
terraform destroy
```
