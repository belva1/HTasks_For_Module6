from multiprocessing import Process, Pool
import requests
import time


def get_url(url):
    response = requests.get(url)
    return response.status_code


if __name__ == '__main__':
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
    pool = Pool(processes=8)
    print(pool.map(get_url, urls))
    print(time.time() - start)
