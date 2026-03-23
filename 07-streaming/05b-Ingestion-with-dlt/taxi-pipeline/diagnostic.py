import requests

url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

r1 = requests.get(url, params={'offset': 0, 'limit': 1}).json()
r2 = requests.get(url, params={'offset': 1000, 'limit': 1}).json()

print(f"Available keys in the data: {r1[0].keys()}")

# Let's find the 'pickup' key regardless of capitalization
pickup_key = [k for k in r1[0].keys() if 'pickup' in k.lower()][0]

val1 = r1[0][pickup_key]
val2 = r2[0][pickup_key]

print(f"Page 1 ({pickup_key}): {val1}")
print(f"Page 2 ({pickup_key}): {val2}")

if val1 == val2:
    print("CRITICAL: The API is ignoring the offset!")
else:
    print("SUCCESS: The API is sending different data.")