# Fuel Price Monitoring & Predictive Analytics Framework

A Data-Driven Framework for Real-Time Fuel Price Monitoring and Predictive Analytics in Uganda’s Liberalized Petroleum Market.

---

## Project Overview
This repository contains the core software engine and implementation framework for a data-driven system designed to eliminate information asymmetry in a liberalized petroleum ecosystem. 

By combining automated tracking and time-series data analysis, this framework monitors pump price fluctuations across key retail distributors (such as Shell, TotalEnergies, Stabex, and Mogas). It identifies pricing anomalies, captures geographic disparities, and generates temporal forecasts to support evidence-based consumer choices and sector policy interventions.

---

## System Architecture (Current Prototype)
The system leverages a decoupled pipeline engineered with **Python** to handle distributed data extraction, cleaning, and structured storage.

```text
 ┌─────────────────┐       ┌────────────────┐       ┌─────────────────┐       ┌──────────────────┐
 │  Data Scrapers  │ ───> │ Data Pipelines │ ────> │  Data Analytics │ ────> │ Visualization    │
 │ (Automation/API)│       │    (Pandas)    │       │  (Linear/LSTM)  │       │  Dashboard UI    │
 └─────────────────┘       └────────────────┘       └─────────────────┘       └──────────────────┘
```

*   **Automation Engine:** Deploys automated data collection scripts to pull live public-facing pricing schedules directly from fuel retailer portals and energy databases.
*   **Data Aggregation Pipeline (`/analytics`):** Orchestrates relational operations and algorithmic normalization via `Pandas` to clean high-volatility raw inputs.
*   **Predictive Analytics Module:** Builds predictive intelligence using baseline data models and time-series networks to map price dependencies and local trends.

---

## Tech Stack & Structure

### Project Blueprint
*   `run.py`: Main execution entry point initializing tracking workers.
*   `schema.sql`: Structural framework mapping data relational models.
*   `.env.example`: Secure token distribution template to prevent secret leakage.

### Technologies Used
*   **Core Logic:** Python 3.11+
*   **Data Science:** Pandas, NumPy, Scikit-Learn
*   **Database Layer:** PostgreSQL Relational Schema

---

##  The Global Scale Vision (Production Roadmap)
While this prototype validates the structural core of the platform using accessible, high-efficiency Python scripting, the **production-grade platform** is architected to transition into a cloud-native, globally distributed system utilizing industry-recognized systems languages.

### 1. High-Concurrency & Distributed Ingestion
*   **Language Transition:** Porting the core data collection tier to **Go (Golang)** or **Rust**.
*   **Objective:** Utilizing Go's native green-thread concurrency (Goroutines) or Rust's zero-cost async safety to manage thousands of concurrent geographically diverse station endpoints without performance bottlenecks.

### 2. Enterprise-Grade API Gateway & Microservices
*   **Language Transition:** Implementing a high-throughput microservice backbone using **Rust (Actix-web / Axum)** or **Node.js (TypeScript)**.
*   **Objective:** Ensuring memory safety, minimal latency footprints, and secure typing patterns for real-time upstream streaming data.

### 3. Stream Processing Infrastructure
*   **Tooling Integration:** Layering **Apache Kafka** or **RabbitMQ** brokers over the database ingestion engine to smoothly buffer high-frequency pricing updates, preventing system stalls during global energy supply shocks.

---

##  Local Development Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd fuel
   ```

2. **Configure Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows PowerShell/bash
   ```

3. **Initialize Environment Variables:**
   ```bash
   cp .env.example .env
   # Configure your local credentials inside your untracked .env file safely
   ```

4. **Prepare Database Instance:**
   ```bash
   psql -U postgres -d fuel_monitoring_system -f schema.sql
   ```
