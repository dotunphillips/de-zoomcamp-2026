#!/usr/bin/env python
"""Run the pipeline and write summary to a file."""

import sys
import os

# Suppress dlt's verbose progress output during execution
os.environ['DLT_PIPELINE_PROGRESS'] = ''

def run_pipeline():
    import dlt
    from dlt.sources.rest_api import rest_api_resources
    from dlt.sources.rest_api.typing import RESTAPIConfig

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

    pipeline = dlt.pipeline(
        pipeline_name='taxi_pipeline',
        destination='duckdb',
        refresh="drop_sources",
        progress="log",
    )

    return pipeline.run(taxi_rest_api_source())


if __name__ == "__main__":
    output_file = "/tmp/pipeline_result.txt"
    
    with open(output_file, 'w') as f:
        f.write("PIPELINE EXECUTION STARTED\n")
        f.flush()
        
        try:
            result = run_pipeline()
            f.write("STATUS: SUCCESS\n")
            f.write(f"Result type: {type(result).__name__}\n")
            if hasattr(result, 'has_failed_jobs'):
                f.write(f"Has failed jobs: {result.has_failed_jobs}\n")
            if hasattr(result, 'loads_ids'):
                f.write(f"Loads IDs: {result.loads_ids}\n")
        except Exception as e:
            f.write(f"STATUS: FAILED\n")
            f.write(f"Exception: {type(e).__name__}\n")
            f.write(f"Message: {str(e)}\n")
            import traceback
            f.write("Traceback:\n")
            traceback.print_exc(file=f)
            sys.exit(1)
    
    print(f"Result written to {output_file}")
