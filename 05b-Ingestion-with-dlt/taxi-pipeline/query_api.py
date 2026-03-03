import requests, json
resp = requests.get('https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api', params={'limit':1,'offset':0})
print('status', resp.status_code)
if resp.status_code==200:
    with open('sample_record.json','w') as f:
        json.dump(resp.json()[0], f, indent=2)
    print('wrote sample_record.json')
else:
    print('request failed')
