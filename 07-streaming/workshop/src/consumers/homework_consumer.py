import json
from kafka import KafkaConsumer

# 1. Setup the connection [cite: 310, 312]
server = 'localhost:9092'
topic_name = 'green-trips'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest', # Start from the beginning 
    group_id='homework-checker',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Decode JSON bytes [cite: 288, 289]
)

print(f"Counting trips in {topic_name}...")

count = 0
try:
    # Kafka consumers are infinite loops by default [cite: 324]
    # We will break once we stop receiving messages for a short period
    for message in consumer:
        # Check the trip_distance field
        if message.value.get('trip_distance', 0) > 5.0:
            count += 1
        
        # Performance tip: Optional print every 1000 matches
        if count % 1000 == 0 and count > 0:
            print(f"Current count: {count}...")
            
except KeyboardInterrupt:
    pass

print(f"Final count of trips with distance > 5: {count}")