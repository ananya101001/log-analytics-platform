# Real-Time Log Analytics Service

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10-2496ED.svg?style=flat&logo=docker)](https://www.docker.com/)
[![Google Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-Serverless-4285F4.svg?style=flat&logo=google-cloud)](https://cloud.google.com/run)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-3.3-231F20.svg?style=flat&logo=apache-kafka)](https://kafka.apache.org/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-23.8-FFCC00.svg?style=flat&logo=clickhouse)](https://clickhouse.com/)

This project is a scalable, real-time log analytics platform built with a modern data stack. It is designed to ingest high-volume log data, process it through a fault-tolerant message queue, and store it in a high-performance analytics database, all deployed on a serverless cloud architecture.

---

## 1. Project Overview

### Problem Statement
Application teams often lack a centralized, real-time system to analyze high-volume log data. This fragmentation can delay incident response, complicate performance monitoring, and prevent effective analysis of user behavior. This project was built to solve that problem by providing a unified and scalable solution.

### Requirements

#### Functional Requirements
- **Ingest** log events from multiple sources.
- **Store** log data efficiently.
- **Provide** an interface for fast, real-time queries.
- **Visualize** key metrics on a dashboard.

#### Non-Functional Requirements
- **Throughput:** Must process over 1 million events per day.
- **Performance:** P99 query latency must be under 400ms.
- **Scalability:** The ingestion service must scale automatically with load.
- **Durability:** The system must guarantee no data loss during ingestion.

---

## 2. System Architecture & Technology Choices

### Architecture Diagram

The architecture is designed to be scalable, durable, and performant, decoupling the log producers from the ingestion and analytics layers.
![System Architecture Diagram](Screenshot 2025-09-08 at 11.55.02 AM.png)

### Technology Justification
*(From Page 2 of the project PDF)*

- **GCP Cloud Run**: Chosen for its serverless, auto-scaling capabilities. It allows us to handle variable log traffic cost-effectively without managing any underlying server infrastructure.
- **Apache Kafka**: Selected as a fault-tolerant message bus. It decouples our log producers from the consumer service, providing a durable buffer that prevents data loss during service outages or traffic spikes.
- **ClickHouse**: Its columnar storage engine is purpose-built for high-speed analytical queries (OLAP). This is critical for meeting the requirement of sub-400ms query performance on large datasets.
- **Prometheus & Grafana**: Chosen as the industry-standard open-source stack for monitoring and visualization.

---

## 3. Project Phases & Key Milestones

This project was built in distinct phases, mirroring a real-world development and deployment lifecycle.

### Phase 1: Local Data Pipeline Success
The core backend services (Kafka, Zookeeper, ClickHouse) were first set up locally using Docker Compose. A Python producer script was used to simulate log generation, and a consumer script successfully processed the data in batches, demonstrating a fully functional local data pipeline.

*(**Action Required:** Add a screenshot from page 7 of your PDF showing the producer sending messages and the consumer inserting batches.)*
`![Local Pipeline Success](local-pipeline-success.png)`

### Phase 2: Containerization & Cloud Deployment
The local Python service was containerized using a `Dockerfile` to create a portable and reproducible environment. The resulting Docker image was built and pushed to Google Artifact Registry. This image was then deployed as a serverless application on **GCP Cloud Run**.

*(**Action Required:** Add the screenshot from page 12 of your PDF showing the successful `gcloud run deploy` command.)*
`![Cloud Run Deployment](cloud-run-deployment.png)`

### Phase 3: End-to-End Connectivity Verified
With the infrastructure running on a GCP Compute Engine VM and the ingestion service live on Cloud Run, the final end-to-end connectivity was verified. The Cloud Run service successfully connected to the remote Kafka and ClickHouse instances, proving the cloud architecture was fully operational.

*(**Action Required:** Add the screenshot of the Cloud Run logs from page 13 showing the successful connections.)*
`![Cloud Run Logs](cloud-run-logs.png)`

---

## 4. Setup and Usage

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Google Cloud SDK (`gcloud` CLI) authenticated to your GCP project.

### Local Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ananya101001/log-analytics-platform.git](https://github.com/ananya101001/log-analytics-platform.git)
    cd log-analytics-platform
    ```
2.  **Start the backend services:**
    This command starts Kafka, Zookeeper, and ClickHouse in Docker containers.
    ```bash
    docker-compose up -d
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the consumer service:**
    In one terminal, start the consumer to listen for messages.
    ```bash
    python app/main.py
    ```
5.  **Run the producer:**
    In a second terminal, run the producer to send test log messages.
    ```bash
    python producer.py
    ```
    You will see the consumer terminal print messages confirming the logs were inserted into ClickHouse.
