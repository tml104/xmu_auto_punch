import asyncio
import aiohttp
import json
import logging


async def send_qq_to_me(msg: str):
    http_url = 'http://127.0.0.1:5700'
    params = {
        "action": "send_private_msg",
        "params": {
            "group_id": 1041159637,
            "message": msg
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(http_url, params=params) as resp:
            logging.info("Sent message to QQ, Response: %s", resp.status)
