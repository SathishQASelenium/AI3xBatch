import requests, json
c = requests.get('http://localhost:8203/api/catalog', timeout=10).json()
for x in c['cards']:
    print(f"{x['key']:35s} {x['category']:12s} {x['target']:8s} {x['title']}")