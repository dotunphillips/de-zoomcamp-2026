import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# 1. Initialize Environment
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1) 
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# 2. Source DDL (Kafka)
# We use a brand new group.id to ensure we read the topic from the very beginning
source_ddl = """
    CREATE TABLE green_trips (
        lpep_pickup_datetime VARCHAR,
        tip_amount FLOAT, 
        event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
        WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'green-trips',
        'properties.bootstrap.servers' = 'redpanda:29092',
        'properties.group.id' = 'flink-tip-final-verification',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json',
        'json.ignore-parse-errors' = 'true'
    )
"""
t_env.execute_sql(source_ddl)

# 3. Sink DDL (Postgres Tip Results)
sink_ddl = """
    CREATE TABLE tip_results (
        window_start TIMESTAMP,
        total_tip FLOAT
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/postgres',
        'table-name' = 'tip_results',
        'username' = 'postgres',
        'password' = 'postgres',
        'driver' = 'org.postgresql.Driver'
    )
"""
t_env.execute_sql(sink_ddl)

# 4. Simple Tumbling Window Logic
# No ORDER BY, no LIMIT. Just pure aggregation per hour.
t_env.execute_sql("""
    INSERT INTO tip_results
    SELECT 
        TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
        SUM(tip_amount) AS total_tip
    FROM green_trips
    GROUP BY 
        TUMBLE(event_timestamp, INTERVAL '1' HOUR)
""")