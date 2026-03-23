import pandas as pd
import json
import time
from kafka import KafkaProducer

# 1. Setup the connection to Redpanda
# In Codespaces, 'localhost:9092' is the external port for your Python script
server = 'localhost:9092' 

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

# 2. Prepare the Data
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
columns = [
    'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 
    'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount', 'total_amount'
]

print("Downloading Green Taxi data for October 2025...")
df = pd.read_parquet(url, columns=columns)

# CRITICAL FIX: Replace all NaN values with None so they become valid JSON 'null'
# This prevents the 'Non-standard token NaN' error in PyFlink
df = df.where(pd.notnull(df), None)

# 3. Execution and Timing
print(f"Sending {len(df)} rows to Redpanda...")
t0 = time.time()

for row in df.to_dict(orient='records'):
    # Convert datetimes to strings for JSON serialization compatibility
    row['lpep_pickup_datetime'] = str(row['lpep_pickup_datetime'])
    row['lpep_dropoff_datetime'] = str(row['lpep_dropoff_datetime'])
    
    producer.send('green-trips', value=row)
producer.send('green-trips', value={'lpep_pickup_datetime': '2025-10-31 23:59:59', 'tip_amount': 0.0})

producer.flush() # Ensure all messages are in the broker before stopping the clock
t1 = time.time()

print(f'Done! Took {(t1 - t0):.2f} seconds')