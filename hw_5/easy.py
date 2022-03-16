#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse


URL = 'https://picsum.photos/200/300'

async def load_image(idx, path):
    async with aiohttp.ClientSession() as session:
        response = await session.get(URL)
        image_bytes = await response.read()
        with open(f'{path}/img_{idx}.jpg', "wb") as f:
            f.write(image_bytes)


async def main(num, path):
    tasks = []
    for i in range(num):
        task = asyncio.create_task(load_image(idx=i, path=path))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", default=5, help="number of uploaded images", type=int)
    parser.add_argument("-p", "--path", default="./artifacts", help="path to save directory")

    args = parser.parse_args()
    asyncio.run(main(num=args.num, path=args.path))
