#!/usr/bin/env python
"""Simple test script to verify the pipeline works."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, '/workspaces/de-zoomcamp-2026/05b-Ingestion-with-dlt/taxi-pipeline')

# Suppress progress output
os.environ['DLT_PIPELINE_PROGRESS'] =''

# Quick test
try:
    # Test 1: Can we import?
    import dlt
    print("✓ dlt imported")
    
    # Test 2: Can we connect to the API?
    import requests
    resp = requests.get(
        "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        params={"limit": 1, "offset": 0},
        timeout=10
    )
    if resp.status_code == 200:
        print("✓ API connection works")
    else:
        print(f"✗ API returned {resp.status_code}")
        sys.exit(1)
    
    # Test 3: Run the actual pipeline
    from taxi_pipeline import taxi_rest_api_source, pipeline
    
    print("Running pipeline...")
    load_info = pipeline.run(taxi_rest_api_source())
    print("✓ Pipeline completed")
    
    # Test 4: Check if data was loaded
    import duckdb
    conn = duckdb.connect('taxi_pipeline.duckdb')
    tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
        
    if tables:
        for table in tables:
            table_name = table[0]
            count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"✓ Table '{table_name}': {count} rows")
    else:
        print("✗ No tables found in database!")
        sys.exit(1)
        
    conn.close()
    print("\n✓ ALL TESTS PASSED")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
