import time

import requests


def get_url(url):
    response = requests.get(url)
    return response.status_code


urls = [
    'https://google.com',
    'https://google.com',
    'https://google.com',
    'https://google.com',
    'https://google.com',
    'https://microsoft.com',
    'https://microsoft.com',
    'https://microsoft.com',
    'https://microsoft.com',
    'https://microsoft.com',
    'https://microsoft.com',
    'https://amazon.com',
    'https://amazon.com',
    'https://amazon.com',
    'https://amazon.com',
    'https://amazon.com',
]

start = time.time()
result = []
for url in urls:
    result.append(get_url(url))

print(result)
print(time.time() - start)

