import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
    #     print("get")
    #     response = await session.get(
    #         'http://127.0.0.1:8080/api/1'
    #     )
    #     print(response.status)
    #     json_data = await response.json()
    #     print(json_data)

        # print("create")
        # response = await session.post(
        #     "http://127.0.0.1:8080/api/", json={"heading": "fasf", "description": "1234", 'user_id': 1}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)
        # print("patch")
        # response = await session.patch(
        #     "http://127.0.0.1:8080/api/11", json={"heading": "user_2",
        #                                           'description': 'dasd',
        #                                           'user_id': 1}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)
        print('DEl')
        response = await session.delete("http://127.0.0.1:8080/api/1")
        print(response.status)
        json_data = await response.json()
        print(json_data)

asyncio.run(main())
