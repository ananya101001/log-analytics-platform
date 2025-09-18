# Real-Time Log Analytics Service

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10-2496ED.svg?style=flat&logo=docker)](https://www.docker.com/)
[![Google Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-Serverless-4285F4.svg?style=flat&logo=google-cloud)](https://cloud.google.com/run)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-3.3-231F20.svg?style=flat&logo=apache-kafka)](https://kafka.apache.org/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-23.8-FFCC00.svg?style=flat&logo=clickhouse)](https://clickhouse.com/)

A scalable, real-time log analytics platform built with a modern data stack. This project ingests high-volume log data, processes it in a fault-tolerant message queue, and stores it in a high-performance analytics database, all deployed on a serverless cloud architecture.

## Problem Statement

[cite_start]Application teams often lack a centralized, real-time system to analyze high-volume log data[cite: 3]. [cite_start]This fragmentation delays incident response, complicates performance monitoring, and prevents effective analysis of user behavior[cite: 4]. This project was built to solve that problem by providing a unified and scalable solution.

## Live Dashboard

Here is a screenshot of the live dashboard, which queries the ClickHouse database in real-time to display the latest ingested logs.

*(**Action Required:** Replace this placeholder with a screenshot of your final UI dashboard!)*

---

## System Architecture

[cite_start]The architecture is designed to be scalable, durable, and performant, decoupling the log producers from the ingestion and analytics layers[cite: 15, 25].


### Core Components:

* [cite_start]**Log Producers:** Any application, server, or mobile app that generates log data[cite: 16].
* [cite_start]**Apache Kafka:** A fault-tolerant message bus that acts as a durable buffer, preventing data loss during traffic spikes or service outages[cite: 17, 25].
* [cite_start]**Python Ingestion Service:** A serverless consumer application running on **GCP Cloud Run** that automatically scales with the volume of incoming logs[cite: 18, 23]. [cite_start]It reads from Kafka and writes data in batches to ClickHouse[cite: 58].
* [cite_start]**ClickHouse:** A high-performance, columnar analytics database purpose-built for fast queries on large datasets, meeting the sub-400ms query latency requirement[cite: 19, 27].
* [cite_start]**Prometheus & Grafana:** An industry-standard stack for monitoring and visualizing system metrics[cite: 21, 22, 28].

---

## Project Phases & Key Milestones

This project was built in three distinct phases, mirroring a real-world development and deployment lifecycle.

### Phase 1: Local Data Pipeline

[cite_start]The core backend services (Kafka, Zookeeper, ClickHouse) were first set up locally using Docker Compose[cite: 33, 36, 37]. [cite_start]A Python producer script was used to simulate log generation, and a consumer script successfully processed the data, demonstrating a fully functional local data pipeline[cite: 194].


### Phase 2: Containerization & Cloud Deployment

[cite_start]The local Python service was containerized using a `Dockerfile`, creating a portable and reproducible environment[cite: 210, 211]. [cite_start]The resulting Docker image was pushed to Google Artifact Registry[cite: 243]. [cite_start]This image was then deployed as a serverless application on **GCP Cloud Run**[cite: 209].


### Phase 3: End-to-End Success

With the infrastructure running on a GCP Compute Engine VM and the ingestion service live on Cloud Run, the final end-to-end test was performed. The Cloud Run service successfully connected to the remote Kafka and ClickHouse instances, proving the entire cloud architecture was fully operational.


---

## Getting Started

### Prerequisites

* Python 3.9+
* Docker & Docker Compose
* [cite_start]Google Cloud SDK (`gcloud` CLI) authenticated to your GCP project[cite: 216].

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ananya101001/log-analytics-platform.git](https://github.com/ananya101001/log-analytics-platform.git)
    cd log-analytics-platform
    ```
2.  **Start the backend services:**
    [cite_start]This command starts Kafka, Zookeeper, and ClickHouse in Docker containers[cite: 38].
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
    [cite_start]You will see the consumer terminal print messages confirming the logs were inserted into ClickHouse[cite: 204, 205, 206, 207].

### Cloud Deployment

1.  [cite_start]**Create GCP Resources:** Set up a Compute Engine VM, static IP address, and firewall rules for Kafka (port 29092) and ClickHouse (port 8123)[cite: 272, 278].
2.  **Run Services on VM:** SSH into the VM, install Docker, and run `docker-compose up -d` using the final `docker-compose.yml` with the static IP address.
3.  **Deploy to Cloud Run:**
    * Build and push the Docker image to Google Artifact Registry.
    * Deploy the image to Cloud Run using the `gcloud run deploy` command, injecting the static IP addresses of the Kafka and ClickHouse services as environment variables.
