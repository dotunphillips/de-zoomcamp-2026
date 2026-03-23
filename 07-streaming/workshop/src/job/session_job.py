import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# 1. Initialize Environment
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1) 
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# 2. Source DDL (Kafka)
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
        'properties.group.id' = 'flink-session-worker',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json',
        'json.ignore-parse-errors' = 'true'
    )
"""
t_env.execute_sql(source_ddl)

# 3. Sink DDL (Postgres) - THIS WAS MISSING IN YOUR PREVIOUS RUN
sink_ddl = """
    CREATE TABLE session_results (
        PULocationID INT,
        num_trips BIGINT,
        window_start TIMESTAMP,
        window_end TIMESTAMP
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/postgres',
        'table-name' = 'session_results',
        'username' = 'postgres',
        'password' = 'postgres',
        'driver' = 'org.postgresql.Driver'
    )
"""
t_env.execute_sql(sink_ddl)

# 4. Session Window Query (Question 5)
t_env.execute_sql("""
    INSERT INTO session_results
    SELECT 
        PULocationID,
        COUNT(*) AS num_trips,
        SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
        SESSION_END(event_timestamp, INTERVAL '5' MINUTE) AS window_end
    FROM green_trips
    GROUP BY 
        PULocationID, 
        SESSION(event_timestamp, INTERVAL '5' MINUTE)
""")