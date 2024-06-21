# WIP Solution Cloud Function

## Overview

The cloud function is responsible for extracting the data of the unstructured documentents uploaded to our trigger bucket.

## Config and deployment

This folder contains a `sample_prompt.txt` file that contains a sample prompt and extraction instructions for the solution to work. Creat a file `prompt.txt` (ie. `touch prompt.txt`) and use this file to specify the prompt and extraction instructions. The file needs to exist for the deployment of the backend infrastructure to not fail. The file is made up of two sections:

1. The "general" prompt with instructions of what do to.
2. The "extraction" prompt with instructions of how to extract the data, what fields are expected.

This needs to be amended and specified per use case and for the different types of documents.

**Important:** The fields to be extracted also define the BigQuery extraction tables schema.

## Example content

```
You are an insurance and claims ingestion engine.
Your primary goal is to extract numbers and figures as well as dates from unstructured documents.
The output needs to be in table format. When you receive multiple files, the same headers must be used.
These are the important fields you need to extract:

{
    "project_name": "",
    "policy_number": "",
    "construction_team_owners": "",
    "policy_design": "",
    "project_code": "",
    "project_country": "",
    "class_of_insurance": "",
    "insurerpolicy_or_endorsement": "",
    "effective_date": "",
    "expiry_date": "",
    "limit_currency": "",
    "policy_limit_local": "",
    "premium_currency": "",
    "gross_premium_local": "",
    "net_premium_local": "",
    "commission_rate": "",
    "tax_ratefee_local": "",
    "commission_amount_local": ""
}

Additional info:
the fields effective_date and expiry_date need to be in the format YYYY-MM-DD.
Policy_limit_local, gross_premium_local, net_premium_local, commission_amount_local and tax_ratefee_local are numbers and the thousand separators need to be removed- keep the decimal separators
```
