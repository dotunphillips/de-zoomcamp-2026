"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: gcp-default

materialization:
  type: table
  strategy: append
@bruin"""

import json
import os
from datetime import datetime
from typing import List, Tuple

import pandas as pd
from dateutil.relativedelta import relativedelta

# NYC Taxi TLC data endpoint
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

def generate_months_to_ingest(start_date: str, end_date: str) -> List[Tuple[int, int]]:
    """Generates a list of (year, month) tuples between start and end dates."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    months = []
    
    curr = start
    while curr < end:
        months.append((curr.year, curr.month))
        curr += relativedelta(months=1)
    return months

def build_parquet_url(taxi_type: str, year: int, month: int) -> str:
    """Constructs the URL for a specific taxi type and month."""
    return f"{BASE_URL}/{taxi_type}_tripdata_{year}-{month:02d}.parquet"

def fetch_trip_data(taxi_type: str, year: int, month: int) -> pd.DataFrame:
    """Fetches a single parquet file and adds tracking columns."""
    url = build_parquet_url(taxi_type, year, month)
    print(f"Fetching: {url}")
    try:
        df = pd.read_parquet(url)
        df['taxi_type'] = taxi_type
        df['extracted_at'] = datetime.now()
        return df
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return pd.DataFrame()

def materialize() -> pd.DataFrame:
    """Main Bruin entry point for Python materialization."""
    # Reads BRUIN_START_DATE and BRUIN_END_DATE from environment variables 
    start_date = os.environ.get("BRUIN_START_DATE")
    end_date = os.environ.get("BRUIN_END_DATE")
    
    # Parses taxi_types from BRUIN_VARS (defaults to ["yellow"]) 
    vars_json = os.environ.get("BRUIN_VARS", "{}")
    pipeline_vars = json.loads(vars_json)
    taxi_types = pipeline_vars.get("taxi_types", ["yellow"])

    # Generates the list of months using generate_months_to_ingest
    months = generate_months_to_ingest(start_date, end_date)
    
    all_frames = []
    
    # Fetches data for each taxi type + month combination 
    for year, month in months:
        for taxi in taxi_types:
            df = fetch_trip_data(taxi, year, month)
            if not df.empty:
                all_frames.append(df)

    # Returns the concatenated DataFrame 
    if not all_frames:
        return pd.DataFrame()
        
    return pd.concat(all_frames, ignore_index=True)