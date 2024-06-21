from cloudevents.http import CloudEvent

import functions_framework
import json
import re
import os
from google.cloud import storage, bigquery
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.api_core.exceptions import NotFound
import vertexai.preview.generative_models as generative_models

# path = "./files/test.pdf"
# prompt = """
# You are a very professional document summarization specialist.
# Please summarize the given document.
# """

# Generate code to open text file on GCS and return content
# project_id = "google.com:marcwo-playground"
# bucket_name = "content_a"
# file_name = "prompt.txt"
# pdf_file = "Quote slip & Wording AGCS 01.12.2023.pdf"

# schema = [
#     bigquery.SchemaField("project_name", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("policy_number", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("construction_team_owners", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("policy_design", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("project_code", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("project_country", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("class_of_insurance", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("insurerpolicy_or_endorsement", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("effective_date", "DATE", mode="NULLABLE"),
#     bigquery.SchemaField("expiry_date", "DATE", mode="NULLABLE"),
#     bigquery.SchemaField("limit_currency", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("policy_limit_local", "NUMERIC", mode="NULLABLE"),
#     bigquery.SchemaField("premium_currency", "STRING", mode="NULLABLE"),
#     bigquery.SchemaField("gross_premium_local", "NUMERIC", mode="NULLABLE"),
#     bigquery.SchemaField("net_premium_local", "NUMERIC", mode="NULLABLE"),
#     bigquery.SchemaField("commission_rate", "NUMERIC", mode="NULLABLE"),
#     bigquery.SchemaField("tax_ratefee_local", "NUMERIC", mode="NULLABLE"),
#     bigquery.SchemaField("commission_amount_local", "NUMERIC", mode="NULLABLE"),
#     bigquery.SchemaField("file_location", "STRING", mode="NULLABLE"),
# ]

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def read_file_from_gcs(project_id, bucket_name, file_name):
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    if blob.exists():
        content = blob.download_as_text()
        return content
    else:
        print(f"File not found: {file_name} in bucket {bucket_name}")
        return None


def generate_content(project_id, bucket_name, file_name, prompt):
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    pdf_file_uri = "gs://" + bucket_name + "/" + file_name
    pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [pdf_file, prompt]
    response = model.generate_content(contents)
    str = re.search(r"```json\n(.*)\n```", response.text, re.DOTALL).group(1).strip()
    response = json.loads(str)
    response[0]["file_location"] = pdf_file_uri
    return response


def create_dataset(project_id, dataset_id):
    client = bigquery.Client(project=project_id)
    """Creates a BigQuery dataset if it doesn't exist."""
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} already exists.")
    except NotFound:
        client.create_dataset(dataset_id)
        print(f"Created dataset {dataset_id}")


def create_table(project_id, dataset_id, table, schema):
    client = bigquery.Client(project=project_id)
    table_ref = project_id + "." + dataset_id + "." + table
    try:
        client.get_table(table_ref)  # Check if table exists
        print(f"Table {table_ref} already exists.")
    except NotFound:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)  # Create table
        print(f"Created table {table.table_id}")


def load_data_to_bq(project_id, dataset_id, table_id, data):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        # autodetect=True,
        # schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    table = f"{project_id}.{dataset_id}.{table_id}"
    load_job = client.load_table_from_json(data, table, job_config=job_config)
    load_job.result()  # Waits for the job to complete.
    print(f"Loaded {load_job.output_rows} rows into {table}")


@functions_framework.cloud_event
def hello_gcs(cloud_event: CloudEvent):
    #     """This function is triggered by a change in a storage bucket.

    #     Args:
    #         cloud_event: The CloudEvent that triggered this function.
    #     Returns:
    #         The event ID, event type, bucket, name, metageneration, and timeCreated.
    #     """
    # Read CloudEvent
    data = cloud_event.data
    # event_id = cloud_event["id"]
    # event_type = cloud_event["type"]
    bucket = data["bucket"]
    name = data["name"]

    # if "prompt.txt" in name.lower():
    #     print("prompt.txt uploaded, ending function early")
    #     return None

    # Generate prompt
    prompt = read_file_from_gcs(
        project_id=os.environ.get("PROJECT_ID"),
        bucket_name=os.environ.get("PROMPT_BUCKET"),
        file_name="prompt.txt",
    )
    extract = generate_content(
        os.environ.get("PROJECT_ID"), bucket_name=bucket, file_name=name, prompt=prompt
    )
    # create_dataset(
    #     project_id=os.environ.get("PROJECT_ID"), dataset_id=os.environ.get("DATASET_ID")
    # )
    # create_table(
    #     project_id=os.environ.get("PROJECT_ID"),
    #     dataset_id=os.environ.get("DATASET_ID"),
    #     table=os.environ.get("TABLE_ID"),
    #     schema=schema,
    # )
    load_data_to_bq(
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        table_id=os.environ.get("TABLE_ID"),
        data=extract,
    )

    # return event_id, event_type, bucket, name, metageneration, timeCreated, updated


# def main(project_id, bucket_name, file_name, pdf_file, dataset_id, table_id, schema):
#     prompt = read_file_from_gcs(project_id, bucket_name, file_name)
#     # print(prompt)
#     response = generate_content(project_id, bucket_name, pdf_file, prompt)
#     print(response)
#     create_dataset(project_id, dataset_id)
#     create_table(project_id, dataset_id, table_id, schema)
#     load_data_to_bq(
#         project_id=project_id,
#         dataset_id=dataset_id,
#         table_id=table_id,
#         data=response,
#     )

#     # print(response)


# if __name__ == "__main__":
#     main(
#         project_id="google.com:marcwo-playground",
#         bucket_name="content_a",
#         file_name="prompt.txt",
#         pdf_file="Quote slip & Wording AGCS 01.12.2023.pdf",
#         schema=schema,
#         dataset_id="test_dataset",
#         table_id="test_table",
#     )
