# Real-Time Log Analytics Service

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10-2496ED.svg?style=flat&logo=docker)](https://www.docker.com/)
[![Google Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-Serverless-4285F4.svg?style=flat&logo=google-cloud)](https://cloud.google.com/run)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-3.3-231F20.svg?style=flat&logo=apache-kafka)](https://kafka.apache.org/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-23.8-FFCC00.svg?style=flat&logo=clickhouse)](https://clickhouse.com/)

This project is a scalable, real-time log analytics platform built with a modern data stack. It is designed to ingest high-volume log data, process it through a fault-tolerant message queue, and store it in a high-performance analytics database, all deployed on a serverless cloud architecture.

## The Business Problem 

In many organizations, critical log data is scattered across different systems, making it difficult to analyze in real-time. This fragmentation delays incident response, complicates performance monitoring, and prevents effective analysis of user behavior. I built this platform to solve that problem by creating a **centralized, scalable, and fast** system that can process over 1 million events per day with a query latency of under 400ms.

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
![System Architecture Diagram](./assets/Screenshot%202025-09-08%20at%2011.55.02%E2%80%AFAM.png)


### Technology Justification

- **GCP Cloud Run**: Chosen for its serverless, auto-scaling capabilities. It allows us to handle variable log traffic cost-effectively without managing any underlying server infrastructure.
- **Apache Kafka**: Selected as a fault-tolerant message bus. It decouples our log producers from the consumer service, providing a durable buffer that prevents data loss during service outages or traffic spikes.
- **ClickHouse**: Its columnar storage engine is purpose-built for high-speed analytical queries (OLAP). This is critical for meeting the requirement of sub-400ms query performance on large datasets.
- **Prometheus & Grafana**: Chosen as the industry-standard open-source stack for monitoring and visualization.

---

## 3. Project Phases & Key Milestones

This project was built in distinct phases, mirroring a real-world development and deployment lifecycle.

### Phase 1: Local Data Pipeline Success
The core backend services (Kafka, Zookeeper, ClickHouse) were first set up locally using Docker Compose. A Python producer script was used to simulate log generation, and a consumer script successfully processed the data in batches, demonstrating a fully functional local data pipeline.

![Screenshot](./assets/Screenshot%202025-09-10%20at%208.18.41%E2%80%AFAM.png)


### Phase 2: Containerization & Cloud Deployment
The local Python service was containerized using a `Dockerfile` to create a portable and reproducible environment. The resulting Docker image was built and pushed to Google Artifact Registry. This image was then deployed as a serverless application on **GCP Cloud Run**.

![Screenshot](./assets/Screenshot%202025-09-17%20at%207.52.45%E2%80%AFPM.png)


### Phase 3: End-to-End Connectivity Verified
With the infrastructure running on a GCP Compute Engine VM and the ingestion service live on Cloud Run, the final end-to-end connectivity was verified. The Cloud Run service successfully connected to the remote Kafka and ClickHouse instances, proving the cloud architecture was fully operational.

![Screenshot](./assets/Screenshot%202025-09-17%20at%2010.10.34%E2%80%AFPM.png)

----




### What I Did:

1.  **Architected a Decoupled System:** I used **Apache Kafka** as a fault-tolerant message queue to buffer incoming data. This is a critical design choice that prevents data loss during traffic spikes and decouples the log producers from the backend processing service.
2.  **Built a Serverless Ingestion Service:** I developed a Python service that consumes data from Kafka and writes it in batches to the database. I containerized this service with **Docker** and deployed it on **GCP Cloud Run**, which allows it to scale automatically and cost-effectively without managing servers.
3.  **Engineered for High-Performance Analytics:** I chose **ClickHouse**, a columnar database, as the storage backend. Its architecture is specifically designed for the high-speed analytical queries required by this project.
4.  **Deployed Infrastructure on GCP:** I provisioned and configured the entire backend infrastructure (Kafka, Zookeeper, ClickHouse) on a **Google Compute Engine VM**, including networking, firewall rules, and static IP management.

## Demonstrating My Skills & Key Milestones 

This project showcases my ability to handle real-world engineering challenges. I took the project from a local prototype to a fully operational cloud service.

### 1. Local Prototyping & Validation

I first built the entire pipeline on my local machine using **Docker Compose** to prove the architecture was sound.


### 2. Cloud Deployment & Containerization

I containerized the application, pushed it to **Google Artifact Registry**, and successfully deployed it as a serverless application on **Cloud Run**.


### 3. Real-World Debugging & Problem Solving

During deployment, I troubleshooted and solved several complex, real-world issues:
* **Networking:** Diagnosed and fixed firewall and IP address misconfigurations between my serverless service and the backend VM.
* **Service Dependencies:** Solved a critical startup race condition where Kafka was crashing because it started before its Zookeeper dependency was fully healthy. I fixed this by implementing a `healthcheck` in the `docker-compose.yml`.
* **Resource Management:** Identified that the ClickHouse database was crashing due to insufficient memory on the VM. I resolved this by stopping the VM, upgrading its machine type to provide more RAM, and restarting the services.

This project demonstrates my end-to-end ability to design, build, deploy, and debug a scalable, cloud-native data system.

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
