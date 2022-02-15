import asyncio
import aiohttp
import json
#import logging
from loguru import logger

import os

HOST = "host.docker.internal" if os.getenv("DOCKER_RUNNING") else "127.0.0.1"
QQID = "1041159637"

async def send_qq_to_me(msg: str):
    http_url = f'http://{HOST}:5700/send_private_msg'
    params = {
        "user_id": QQID,
        "message": msg
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(http_url, data=params) as resp:
            logger.info("Sent message to QQ, Response: {}", resp.status)
