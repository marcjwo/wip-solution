# WIP Solution Cloud Function

## Overview

The cloud function is responsible for extracting the data of the unstructured documentents uploaded to our trigger bucket.

## Config and deployment

This folder contains a `sample_prompt.txt` file that contains a sample prompt and extraction instructions for the solution to work. Create a file `prompt.txt` (ie. `touch prompt.txt`) and use this file to specify the prompt and extraction instructions. The file needs to exist for the deployment of the backend infrastructure to not fail. The file is made up of two sections:

1. The "general" prompt with instructions of what do to.
2. The "extraction" prompt with instructions of how to extract the data, what fields are expected.

This needs to be amended and specified per use case and for the different types of documents.

**Important:** The fields to be extracted also define the BigQuery extraction tables schema.

## Example content

````
You are an AI assistant skilled at analyzing financial documents. Your task is to extract the most important information from an earnings report and present it in a structured, tabular format. Please include the following details:

1. **Company Information:**
  - Company Name
  - Ticker Symbol
  - Report Date
  - Reporting Period

2. **Financial Metrics:**
  - Revenue
  - Net Income
  - Earnings Per Share (EPS)
  - Operating Income
  - Total Assets
  - Total Liabilities

3. **Key Highlights:**
  - Major Achievements
  - Challenges Faced
  - Strategic Initiatives
  - Guidance and Outlook

4. **Sentiment Analysis:**
  - Overall Sentiment (Positive, Neutral, Negative)
  - Key Sentiment Drivers

5. **Summary:**
  - Executive Summary of the Earnings Report

Please extract this information and format it as a JSON object with the structure defined below. Perform sentiment analysis on the textual content to provide an overall sentiment rating and identify key sentiment drivers. Provide concise and accurate summaries for each section.

**Output JSON Structure:**

```json
{
  "company_name": "string",
  "ticker_symbol": "string",
  "report_date": "YYYY-MM-DD",
  "reporting_period": "YYYY-MM-DD",
  "revenue": "number",
  "net_income": "number",
  "eps": "number",
  "operating_income": "number",
  "total_assets": "number",
  "total_liabilities": "number",
  "achievements": "string",
  "challenges": "string",
  "strategic_initiatives": "string",
  "guidance_and_outlook": "string"
  "overall_sentiment": "string",
  "key_sentiment_drivers": "string",
  "summary": "string"
}
```
````
