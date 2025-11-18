import json
from pathlib import Path
from typing import List, Dict, Any

from app.core.config import get_settings
from app.databases.redis_client import get_redis_store

settings = get_settings()

SEED_JSON_PATH = Path(__file__).parent.parent / settings.SEED_JSON_PATH

def load_seed_file() -> List[Dict[str, Any]]:
    """Read and parse the seed JSON file with user profiles."""
    if not SEED_JSON_PATH.exists():
        raise FileNotFoundError(f"Seed file not found: {SEED_JSON_PATH}")

    with SEED_JSON_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Seed JSON must contain a list of user profiles.")

    return data

def validate_user_profile(profile: Dict[str, Any]) -> None:
    """Basic validation to ensure minimal required fields exist."""
    required_fields = ["user_id", "name", "role", "company"]

    missing = [field for field in required_fields if field not in profile]
    if missing:
        raise ValueError(f"User profile missing required fields: {missing} (profile: {profile})")

async def save_profiles_to_redis(profiles: List[Dict[str, Any]]) -> None:
    redis_store = get_redis_store().store

    for profile in profiles:
        validate_user_profile(profile)

        user_id = profile["user_id"]
        key = f"{settings.USER_KEY_PREFIX}{user_id}"

        await redis_store.json().set(key, "$", profile)

        # Add index
        await redis_store.sadd(settings.USER_INDEX_KEY, user_id)

        print(f"[OK] Stored profile JSON for {user_id}")

async def run():
    print(f"Loading user profiles from: {SEED_JSON_PATH}")
    profiles = load_seed_file()
    print(f"Found {len(profiles)} profiles in seed file.")

    await save_profiles_to_redis(profiles)

    print("Done. All user profiles stored in Redis.")