from redis import asyncio as aioredis
from src.config import CONFIG

JTI_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=CONFIG.REDIS_HOST, port=CONFIG.REDIS_PORT, db=0
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(jti, "", ex=JTI_EXPIRY)


async def check_jti_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None
