import requests, json
URL="http://suggestqueries.google.com/complete/search?client=firefox&q=google"
headers = {'User-agent':'Mozilla/5.0'}
response = requests.get(URL, headers=headers)
result = json.loads(response.content.decode('utf-8'))
print(result)
