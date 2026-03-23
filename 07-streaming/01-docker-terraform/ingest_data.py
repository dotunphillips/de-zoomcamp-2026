#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import os

@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5433, type=int, help='PostgreSQL port') # Updated to your 5433
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--url', help='URL of the parquet file') # Simplified to take a direct URL
@click.option('--chunksize', default=100000, type=int, help='Size of the chunks')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, url, chunksize):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # --- TASK 1: GREEN TAXI DATA (PARQUET) ---
    file_name = 'green_trips.parquet'
    os.system(f"wget {url} -O {file_name}")
    df = pd.read_parquet(file_name)
    
    # Date conversion (Green Taxi uses 'lpep')
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Ingest in chunks
    df.to_sql(name=target_table, con=engine, if_exists='replace', index=False, chunksize=chunksize)
    print(f"Successfully ingested {target_table}")

    # --- TASK 2: ZONE LOOKUP DATA (CSV) ---
    z_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi+_zone_lookup.csv"
    df_zones = pd.read_csv(z_url)
    df_zones.to_sql(name='zones', con=engine, if_exists='replace', index=False)
    print("Successfully ingested zones table")

    if __name__ == '__main__':
        run()