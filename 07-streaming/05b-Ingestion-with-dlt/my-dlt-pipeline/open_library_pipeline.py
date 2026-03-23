"""Template for building a `dlt` pipeline to ingest data from a REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


# if no argument is provided, `access_token` is read from `.dlt/secrets.toml`
@dlt.source
def open_library_rest_api_source(access_token: str = dlt.secrets.value):
    """Define dlt resources from REST API endpoints."""
    config: RESTAPIConfig = {
        "client": {
            # base URL for the Open Library REST API
            "base_url": "https://openlibrary.org/",
            # no authentication required for the public endpoints
        },
        # apply some defaults to all resources (optional)
        "resource_defaults": {
            "endpoint": {
                # always request json data
                "params": {
                    "format": "json",
                    "jscmd": "data"
                }
            }
        },
        "resources": [
            # single resource for the books endpoint
            {
                "name": "books",
                "endpoint": {
                    "path": "api/books",
                    "method": "GET",
                    # example query for a single ISBN; users can modify later
                    "params": {
                        "bibkeys": "ISBN:0451526538"
                    },
                    # the API returns a dict keyed by the bibkey – select all values
                    "data_selector": "*"
                }
            }
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name='open_library_pipeline',
    destination='duckdb',
    # `refresh="drop_sources"` ensures the data and the state is cleaned
    # on each `pipeline.run()`; remove the argument once you have a
    # working pipeline.
    refresh="drop_sources",
    # show basic progress of resources extracted, normalized files and load-jobs on stdout
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(open_library_rest_api_source())
    print(load_info)  # noqa: T201
