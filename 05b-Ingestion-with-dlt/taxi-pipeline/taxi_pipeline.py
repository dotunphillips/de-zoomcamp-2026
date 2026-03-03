import dlt
import requests

@dlt.resource(name="taxi_rides", write_disposition="replace")
def taxi_data():
    url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    for i in range(10):
        offset = i * 1000
        # The API is picky; we manually build the query string
        full_url = f"{url}?offset={offset}&limit=1000"
        print(f"Loading page {i+1}: {full_url}")
        
        response = requests.get(full_url)
        data = response.json()
        if not data:
            break
        yield data

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data_set", # This is the SCHEMA name
    )
    pipeline.run(taxi_data())