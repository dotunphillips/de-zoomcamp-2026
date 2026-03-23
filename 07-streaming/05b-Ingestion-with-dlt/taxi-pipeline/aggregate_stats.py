import requests
from datetime import datetime

url = 'https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api'
offset = 0
limit = 1000

min_date = None
max_date = None
count = 0
cc_count = 0
sum_tips = 0.0

while True:
    resp = requests.get(url, params={'limit': limit, 'offset': offset})
    if resp.status_code != 200:
        print('request failed', resp.status_code)
        break
    data = resp.json()
    if not data:
        break
    for rec in data:
        count += 1
        pay = rec.get('payment_type','').upper()
        if pay.startswith('CREDIT'):
            cc_count += 1
        tip = rec.get('tip_amt')
        try:
            sum_tips += float(tip) if tip is not None else 0.0
        except Exception:
            pass
        dt_str = rec.get('Trip_Pickup_DateTime')
        if dt_str:
            try:
                dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                if min_date is None or dt < min_date:
                    min_date = dt
                if max_date is None or dt > max_date:
                    max_date = dt
            except Exception:
                pass
    offset += limit

print('count', count)
print('date range', min_date, max_date)
print('cc proportion', cc_count/count if count else None)
print('total tips', sum_tips)
