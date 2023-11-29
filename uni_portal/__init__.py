import asyncio
from time import sleep


async def pr():
    for i in range(3):
        sleep(1)
        print(i)


asyncio.ensure_future(pr())
