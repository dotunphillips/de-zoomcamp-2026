#!/usr/bin/env python
"""Debug version of the taxi pipeline with error handling."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig
import sys


@dlt.source
def taxi_rest_api_source():
    """Define dlt resources from NYC taxi API."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resources": [
            {
                "name": "taxi_data",
                "endpoint": {
                    "path": "",
                    "method": "GET",
                    "paginator": {
                        "type": "offset",
                        "offset_param": "offset",
                        "limit": 1000,
                        "limit_param": "limit",
                        "stop_after_empty_page": True,
                    },
                    "data_selector": None,
                },
                "primary_key": None,
                "write_disposition": "append",
            }
        ],
    }

    yield from rest_api_resources(config)


if __name__ == "__main__":
    try:
        pipeline = dlt.pipeline(
            pipeline_name='taxi_pipeline',
            destination='duckdb',
            refresh="drop_sources",
            progress="log",
        )
        
        print("Pipeline created successfully")
        sys.stdout.flush()
        
        load_info = pipeline.run(taxi_rest_api_source())
        
        # Instead of printing the full load_info, just print summary
        print(f"\n✓ Pipeline completed successfully")
        print(f"Pipeline name: {pipeline.pipeline_name}")
        print(f"Destination: {pipeline.destination}")
        
        # Check the loaded tables
        import duckdb
        conn = duckdb.connect(pipeline.dataset_name + ".duckdb")
        tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
        
        for table in tables:
            table_name = table[0]
            count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"Table '{table_name}': {count} rows loaded")
        
        conn.close()
        
    except Exception as e:
        print(f"\n✗ Error occurred: {type(e).__name__}")
        print(f"Message: {str(e)}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        sys.exit(1)
