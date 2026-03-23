# Data Engineering Zoomcamp - Module 6 Homework (Spark)

This repository contains my solution for the Module 6 Spark homework, executed in a GitHub Codespace environment with Google Cloud Storage integration.

## Project Structure
- `homework.ipynb`: Main Jupyter Notebook containing data ingestion, repartitioning, and analysis.
- `data/pq/yellow/2025/11`: Spark partitioned output (local storage).
- `.gitignore`: Configured to exclude large data files and CSVs.

## Analysis Results
- **Spark Version:** 4.1.1
- **November 15th Trips:** 162,604
- **Longest Trip:** 90.65 hours
- **Least Frequent Pickup Zone:** Governor's Island/Ellis Island/Liberty Island

## Technical Notes
- Used `unix_timestamp` for duration calculations to handle `TIMESTAMP_NTZ` data types.
- Configured Spark with `local[*]` to utilize all available cores in the Codespace.