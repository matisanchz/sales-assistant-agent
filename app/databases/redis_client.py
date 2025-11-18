from datetime import datetime
from functools import lru_cache
import json
import redis.asyncio as redis
from typing import List

from app.core.config import get_settings

settings = get_settings()

class RedisBaseStore():
    def __init__(self):
        self.store = redis.from_url(settings.REDIS_URL)

async def save_chat_history(key: str, messages: List[dict], ttl: int, title: str = None):
    # Metadata for title and creation time
    meta_key = f"{key}:meta"

    exists = await get_redis_store().store.exists(meta_key)
    if not exists:
        meta = {
            "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "title": title or "Untitled Session"
        }
        await get_redis_store().store.hset(meta_key, mapping=meta)
    else:
        fields = {
            "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "title": title or "Untitled Session"
        }
        await get_redis_store().store.hset(meta_key, mapping=fields)

    await get_redis_store().store.expire(meta_key, ttl)
    
    await get_redis_store().store.rpush(key, *[json.dumps(m) for m in messages])
    await get_redis_store().store.expire(key, ttl)

    length = await get_redis_store().store.llen(key)
    if length > 100:
        await get_redis_store().store.ltrim(key, -100, -1)

async def get_chat_history(key: str) -> list[dict]:
    meta_key = str(key+":meta")
    title = await get_current_title(meta_key)

    raw_list = await get_redis_store().store.lrange(key, 0, -1)
    history = []
    for item in raw_list:
        try:
            item_str = item.decode("utf-8")
            history.append(json.loads(item_str))
        except json.JSONDecodeError:
            pass
    return history, title

async def get_current_title(meta_key):
    """
    Retrieve session metadata title stored in key:meta.
    Returns a dict or None if not found/invalid.
    """
    raw_meta = await get_redis_store().store.hgetall(meta_key)
    if not raw_meta:
        return None

    try:
        meta = {k.decode("utf-8"): v.decode("utf-8") for k, v in raw_meta.items()}
        return meta.get("title", "Untitled Session")
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    
async def get_user_profile(user_id: str) -> dict | None:
    redis_store = get_redis_store().store
    key = f"{settings.USER_KEY_PREFIX}{user_id}"
    
    return await redis_store.json().get(key)
    
@lru_cache
def get_redis_store() -> RedisBaseStore:
    return RedisBaseStore()