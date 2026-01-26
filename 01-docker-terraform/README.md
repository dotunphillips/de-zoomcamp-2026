# Data Engineering Zoomcamp 2026 - Module 1 Homework

This repository contains the solution for the first module of the Data Engineering Zoomcamp.

## Project Structure
* `terraform/`: GCP Infrastructure as Code files.
* `docker/`: Docker Compose configuration for Postgres and pgAdmin.
* `sql/`: SQL queries used for the homework questions.

---

## Question 1: Understanding Docker images
Command: `docker run -it --rm --entrypoint=bash python:3.13`
Check version: `pip --version`
**Answer:** `25.3`

## Question 2: Understanding Docker networking and docker-compose
Based on the provided `docker-compose.yaml`, pgAdmin connects to the database service using the service name and the internal port.
**Answer:** `db:5432`

## SQL Homework Queries (November 2025 Green Taxi Data)

### Question 3: Counting short trips
```sql
SELECT count(*) 
FROM green_tripdata 
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```
### Question 4: Longest trip for each day
```sql
SELECT CAST(lpep_pickup_datetime AS DATE) AS pickup_day, 
       MAX(trip_distance) AS max_dist
FROM green_tripdata
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_dist DESC
LIMIT 1;
```
### Question 5: Biggest pickup zone
```sql
SELECT z."Zone", SUM(t.total_amount) as total
FROM green_tripdata t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE CAST(t.lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total DESC
LIMIT 1;
```

### Question 6: Largest tip
```sql 
SELECT zd."Zone" as dropoff_zone, MAX(t.tip_amount) as max_tip
FROM green_tripdata t
JOIN zones zp ON t."PULocationID" = zp."LocationID"
JOIN zones zd ON t."DOLocationID" = zd."LocationID"
WHERE zp."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01' 
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY dropoff_zone
ORDER BY max_tip DESC
LIMIT 1;
```

### Question 7: Terraform Workflow
**Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`