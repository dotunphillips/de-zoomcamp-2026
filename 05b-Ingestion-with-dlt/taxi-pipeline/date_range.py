import requests
from datetime import datetime

url = 'https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api'
offset = 0
limit = 1000
min_date = None
max_date = None

while True:
    resp = requests.get(url, params={'limit': limit, 'offset': offset})
    if resp.status_code != 200:
        print('request failed', resp.status_code)
        break
    data = resp.json()
    if not data:
        break
    for rec in data:
        # parse pickup date
        dt_str = rec.get('Trip_Pickup_DateTime')
        if dt_str:
            try:
                dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            except Exception:
                continue
            if min_date is None or dt < min_date:
                min_date = dt
            if max_date is None or dt > max_date:
                max_date = dt
    offset += limit
    # stop if offset is large to avoid long run
    if offset > 100000:  # sample limit
        break

print('min_date', min_date)
print('max_date', max_date)
