# -*- coding: utf-8 -*-
"""Rate limiting and concurrency control for Telegram bot."""
import asyncio
import time
from collections import defaultdict

# Allow at most 5 heavy document parsing tasks concurrently
GLOBAL_PROCESSING_SEMAPHORE = asyncio.Semaphore(5)

# Per-user timestamps of recent uploads
_user_upload_times = defaultdict(list)

# Limits: max 10 uploads within 30 seconds per user
MAX_UPLOADS_WINDOW = 30  # seconds
MAX_UPLOADS_COUNT = 10


def check_rate_limit(user_id: int) -> tuple[bool, int]:
    """
    Checks if a user is within upload rate limits.
    Returns (is_allowed, wait_seconds).
    """
    now = time.time()
    times = _user_upload_times[user_id]

    # Filter out timestamps older than the window
    _user_upload_times[user_id] = [t for t in times if now - t < MAX_UPLOADS_WINDOW]
    current_count = len(_user_upload_times[user_id])

    if current_count >= MAX_UPLOADS_COUNT:
        oldest = _user_upload_times[user_id][0]
        wait_seconds = int(MAX_UPLOADS_WINDOW - (now - oldest)) + 1
        return False, max(1, wait_seconds)

    _user_upload_times[user_id].append(now)
    return True, 0
