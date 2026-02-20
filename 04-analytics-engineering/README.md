# NYC Taxi Analytics Pipeline - DE Zoomcamp Week 4

This project demonstrates the use of dbt (Data Build Tool) with Google BigQuery to transform raw NYC Taxi and FHV data into analytical tables.

## Project Details
* **GCP Project ID:** `tactile-anthem-485519-v6`
* **Target Dataset:** `dbt_prod`
* **dbt Version:** 1.11.0-post29



---

## Homework Solutions & Documentation

### Question 1: dbt Selection Syntax
**Selection:** `int_trips_unioned only`
* **Reasoning:** The command `dbt run --select int_trips_unioned` target only the specific model named. To include dependencies, operators like `+` or `*` would be required.

### Question 2: dbt Testing Behavior
**Selection:** `dbt fails the test with non-zero exit code`
* **Reasoning:** In dbt, an `accepted_values` test on a column like `payment_type` will trigger an error if a value outside the defined list (like 6) appears. A failed test results in a non-zero exit code to prevent downstream corruption.

### Question 3: Record Count for Monthly Zone Revenue
**Query:**
```sql
SELECT count(*) 
FROM `tactile-anthem-485519-v6.dbt_prod.fct_monthly_zone_revenue`;
```
### Question 4: Best Performing Zone (Green Taxi 2020)
**Query:**
```sql
SELECT 
    pickup_zone, 
    SUM(revenue_monthly_total_amount) as total_revenue
FROM `tactile-anthem-485519-v6.dbt_prod.fct_monthly_zone_revenue`
WHERE service_type = 'Green' AND year = 2020
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;
```
### Question 5: Total Green Trips (October 2019)
**Query:**
```sql
SELECT sum(total_monthly_trips) 
FROM `tactile-anthem-485519-v6.dbt_prod.fct_monthly_zone_revenue`
WHERE service_type = 'Green' 
  AND year = 2019 
  AND month = 10;
```
### Question 6: FHV Staging Record Count
**Query:**
```sql
SELECT count(*) 
FROM `tactile-anthem-485519-v6.dbt_prod.stg_fhv_tripdata`;
```