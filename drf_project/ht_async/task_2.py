import asyncio
import time
import sys
sys.set_int_max_str_digits(10000000)


async def power(number):
    return number ** 1_000_000


async def main():
    print(f"started at {time.strftime('%X')}")
    result = await asyncio.gather(
        power(2),
        power(3),
        power(5),
    )
    print(result)
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())