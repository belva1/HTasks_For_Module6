import time
from threading import Thread
import requests


def get_url(url):
    response = requests.get(url)
    print(response.status_code)


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
threads = []
for url in urls:
    cur_thread = Thread(target=get_url, args=(url,))
    threads.append(cur_thread)
    cur_thread.start()
for thread in threads:
    thread.join()  # waiting for the end of working of every thread

print(time.time() - start)