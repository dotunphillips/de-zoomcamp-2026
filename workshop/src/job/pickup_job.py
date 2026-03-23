import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# Initialize Flink
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1) # Required for single partition [cite: 58]
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# Source DDL: Reading from 'green-trips' [cite: 129]
source_ddl = """
    CREATE TABLE green_trips (
        lpep_pickup_datetime VARCHAR,
        PULocationID INT,
        event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
        WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'green-trips',
        'properties.bootstrap.servers' = 'redpanda:29092',
        'properties.group.id' = 'flink-worker-v3', -- Changed group ID to start fresh
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json',
        'json.ignore-parse-errors' = 'true',
        'json.fail-on-missing-field' = 'false'
    )
"""
t_env.execute_sql(source_ddl)

# Sink DDL: Writing to Postgres [cite: 66]
sink_ddl = """
    CREATE TABLE trips_by_pickup (
        window_start TIMESTAMP,
        PULocationID INT,
        num_trips BIGINT
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/postgres',
        'table-name' = 'trips_by_pickup',
        'username' = 'postgres',
        'password' = 'postgres',
        'driver' = 'org.postgresql.Driver'
    )
"""
t_env.execute_sql(sink_ddl)

# Tumbling Window Query [cite: 141]
t_env.execute_sql("""
    INSERT INTO trips_by_pickup
    SELECT 
        TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
        PULocationID, 
        COUNT(*) AS num_trips
    FROM green_trips
    GROUP BY 
        PULocationID, 
        TUMBLE(event_timestamp, INTERVAL '5' MINUTE)
""")