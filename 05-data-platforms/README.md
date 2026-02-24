# Data Engineering Zoomcamp 2026: Module 5 (Data Platforms)
## Homework Submission: Bruin Pipeline Implementation

This repository contains the implementation of a NYC Taxi data pipeline using the Bruin data platform. This README documents the project structure and provides the verified answers for the Module 5 homework.

---

### 1. Project Overview
The pipeline ingests raw NYC taxi data, cleans it via a staging layer, and produces an analytical report. It is configured to run on both local DuckDB for development and Google BigQuery for production.

### 2. Homework Answer Key

#### Question 1: Bruin Pipeline Structure
**Answer:** `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`  
**Explanation:** Bruin requires a root `.bruin.yml` for project-wide settings and a `pipeline/` directory containing the `pipeline.yml` definition and the `assets/` folder for transformations.

#### Question 2: Materialization Strategies
**Answer:** `time_interval` - incremental based on a time column  
**Explanation:** For data partitioned by time (like months), `time_interval` is the most efficient strategy as it allows Bruin to replace specific time buckets without rebuilding the entire table.

#### Question 3: Pipeline Variables
**Answer:** `bruin run --var 'taxi_types=["yellow"]'`  
**Explanation:** Bruin uses the `--var` flag to override variables defined in `pipeline.yml`. Since `taxi_types` is an array, the value must be passed as a valid JSON-style string.

#### Question 4: Running with Dependencies
**Answer:** `bruin run --select ingestion.trips+`  
**Explanation:** The `--select` flag identifies assets by their metadata name. The `+` suffix is the specific operator used to include the asset and all its **downstream** children in the execution.

#### Question 5: Quality Checks
**Answer:** `name: not_null`  
**Explanation:** To ensure a column contains no empty values, the `not_null` check is the built-in validator used in the asset metadata block.

#### Question 6: Lineage and Dependencies
**Answer:** `bruin lineage`  
**Explanation:** The `bruin lineage` command generates the metadata required to visualize or list the dependencies between different assets in the DAG.

#### Question 7: First-Time Run
**Answer:** `--full-refresh`  
**Explanation:** When initializing a database or overwriting existing structures to start fresh, the `--full-refresh` flag ignores incremental logic and creates all tables from scratch.

---

### 3. Implementation

#### Connection Configuration (`.bruin.yml`)
My project is configured with the following active connections:
* `gcp-default`: BigQuery (Production)
* `duckdb-default`: DuckDB (Local Development)

#### Asset Definition Example
Below is the metadata configuration used for the staging layer to ensure data quality and correct materialization:

```sql
/* @bruin
name: staging.trips
type: bq.sql
connection: gcp-default
materialization:
  type: table
  strategy: time_interval
checks:
  - name: not_null
    column: pickup_datetime
@bruin */