# AI-Powered Financial Transaction Anomaly Detection

An automated financial transaction anomaly detection prototype built using Python, Isolation Forest, FastAPI, PostgreSQL, n8n, Ollama, and Gmail.

## Project Overview

This project processes a synthetic financial transaction dataset, identifies anomalous transactions, generates AI explanations, stores alerts in PostgreSQL, and sends email notifications through n8n.

## Technology Stack

- Python and Pandas
- Scikit-learn (Isolation Forest)
- FastAPI and Uvicorn
- PostgreSQL
- n8n
- Ollama (Llama 3.2 3B)
- Gmail API
- Docker

## Architecture

Transaction CSV
    |
    v
Python Data Quality Checks
    |
    v
Isolation Forest
    |
    v
FastAPI + n8n
    |
    v
PostgreSQL
    |
    v
Ollama AI Explanation
    |
    v
Gmail Notification

## Model Evaluation

| Metric | Result |
|---|---|
| Total transactions | 1,000 |
| Detected anomalies | 50 |
| Precision | 0.980 |
| Recall | 0.980 |
| F1 Score | 0.980 |

Metrics were calculated against synthetic anomaly labels on the same dataset used to fit the model. They do not represent performance on unseen financial transactions.

## Features

- Automated data quality validation
- Isolation Forest anomaly detection
- REST API integration with FastAPI
- n8n workflow orchestration
- PostgreSQL alert storage
- AI-generated anomaly explanations
- Gmail email alerts
- Duplicate-notification claim tracking
- Gmail success and failure branches

## Local Setup

1. Install Python and Docker Desktop.
2. Install and configure n8n, PostgreSQL, and Ollama.
3. Create a Python virtual environment.
4. Install dependencies:

   pip install -r requirements.txt

5. Start FastAPI:

   uvicorn src.api:app --reload --port 8000

6. Import the exported n8n workflow.
7. Configure PostgreSQL and Gmail credentials.
8. Test the workflow manually before enabling scheduling.

## Limitations

- Processes a static synthetic CSV dataset.
- Model is retrained on the input dataset for each detection run.
- Isolation Forest scores are not fraud probabilities.
- AI explanations may require additional context to support their claims.
- Exactly-once email delivery is not guaranteed.
- Automatic scheduling requires the local services to remain running.

## Future Improvements

- Live transaction ingestion
- Model evaluation on unseen data
- Monitoring dashboard
- Automated recovery and retry handling
- Cloud deployment

## Project Status

Functional local batch-processing prototype.
