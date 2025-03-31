import requests
url = "https://api.github.com/search/users"
query = "location:London followers:>70"
headers = {"User-Agent": "GA4-Q7-Request"}

response = requests.get(url, headers=headers, params={"q": query, "per_page": 5})  
print("Status Code:", response.status_code)
print("Response JSON:", response.json())