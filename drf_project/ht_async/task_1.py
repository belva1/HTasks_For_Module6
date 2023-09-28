import time
import aiohttp
import asyncio


async def fetch_url(name, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)
            print(await response.text())


async def main():
    print(f"started at {time.strftime('%X')}")
    await asyncio.gather(
        fetch_url("google1", 'https://google.com'),
        fetch_url("google2", 'https://google.com'),
        fetch_url("google3", 'https://google.com'),
        fetch_url("google4", 'https://google.com'),
        fetch_url("google5", 'https://google.com'),
        fetch_url("amazon1", 'https://amazon.com'),
        fetch_url("amazon2", 'https://amazon.com'),
        fetch_url("amazon3", 'https://amazon.com'),
        fetch_url("amazon4", 'https://amazon.com'),
        fetch_url("amazon5", 'https://amazon.com'),
        fetch_url("microsoft1", 'https://microsoft.com'),
        fetch_url("microsoft2", 'https://microsoft.com'),
        fetch_url("microsoft3", 'https://microsoft.com'),
        fetch_url("microsoft4", 'https://microsoft.com'),
        fetch_url("microsoft5", 'https://microsoft.com'),
    )
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())