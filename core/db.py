# -*- coding: utf-8 -*-
"""SQLite database management for Asosnoma bot users, stats, and generations."""
import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "bot.db"


def _get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables in sqlite database."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_blocked INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lang TEXT,
                reports TEXT,
                total_sources INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                full_name TEXT,
                message_text TEXT,
                replied INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def upsert_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Inserts a new user or updates their last_active and details."""
    import config
    if username and username.lower() == config.ADMIN_USERNAME.lower():
        set_admin_id(user_id)
    with _get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, joined_at, last_active, is_blocked)
            VALUES (?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(user_id) DO UPDATE SET
                username = COALESCE(excluded.username, users.username),
                first_name = COALESCE(excluded.first_name, users.first_name),
                last_name = COALESCE(excluded.last_name, users.last_name),
                last_active = ?,
                is_blocked = 0
        """, (user_id, username, first_name, last_name, now, now, now))
        conn.commit()


def log_generation(user_id: int, lang: str, reports: str, total_sources: int):
    """Records a generated document."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO generations (user_id, lang, reports, total_sources, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, lang, reports, total_sources, now))
        conn.commit()


def set_user_blocked(user_id: int, blocked: bool = True):
    """Marks a user as blocked bot or active."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_blocked = ? WHERE user_id = ?", (1 if blocked else 0, user_id))
        conn.commit()


def get_all_active_users():
    """Returns list of all non-blocked user IDs."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE is_blocked = 0")
        return [row['user_id'] for row in cursor.fetchall()]


def get_stats():
    """Returns system stats dictionary."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        # 1. Total users
        cursor.execute("SELECT COUNT(*) AS cnt FROM users")
        total_users = cursor.fetchone()['cnt']

        # 2. Blocked users
        cursor.execute("SELECT COUNT(*) AS cnt FROM users WHERE is_blocked = 1")
        blocked_users = cursor.fetchone()['cnt']

        # 3. Active today
        cursor.execute("""
            SELECT COUNT(*) AS cnt FROM users 
            WHERE DATE(last_active) = DATE('now', 'localtime')
        """)
        active_today = cursor.fetchone()['cnt']

        # 4. Total generations
        cursor.execute("SELECT COUNT(*) AS cnt FROM generations")
        total_generations = cursor.fetchone()['cnt']

        # 5. Last 5 users
        cursor.execute("""
            SELECT user_id, username, first_name, last_active 
            FROM users 
            ORDER BY last_active DESC LIMIT 5
        """)
        recent_users = [dict(row) for row in cursor.fetchall()]

        return {
            'total_users': total_users,
            'blocked_users': blocked_users,
            'active_today': active_today,
            'total_generations': total_generations,
            'recent_users': recent_users
        }


def get_setting(key: str, default: str = None) -> str:
    """Gets a setting value from settings table."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row['value'] if row else default


def set_setting(key: str, value: str):
    """Sets a setting value in settings table."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, value))
        conn.commit()


def get_admin_id() -> int:
    """Returns Telegram chat ID of the bot admin."""
    import config
    if config.ADMIN_ID and config.ADMIN_ID > 0:
        return config.ADMIN_ID
    val = get_setting('admin_id')
    if val and val.isdigit():
        return int(val)
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE LOWER(username) = LOWER(?) LIMIT 1", (config.ADMIN_USERNAME,))
        row = cursor.fetchone()
        if row:
            return row['user_id']
    return 0


def set_admin_id(user_id: int):
    """Caches admin user_id in settings."""
    import config
    config.ADMIN_ID = user_id
    set_setting('admin_id', str(user_id))


def save_feedback(user_id: int, username: str, full_name: str, message_text: str) -> int:
    """Saves user feedback and returns the record ID."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO feedback (user_id, username, full_name, message_text, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, full_name, message_text, now))
        conn.commit()
        return cursor.lastrowid


def get_users_list(limit: int = 20, offset: int = 0) -> list:
    """Returns list of users with username, name, last active, and generation count."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.user_id, u.username, u.first_name, u.last_name, u.last_active, u.joined_at, u.is_blocked,
                   (SELECT COUNT(*) FROM generations g WHERE g.user_id = u.user_id) AS gen_count
            FROM users u
            ORDER BY u.last_active DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        return [dict(row) for row in cursor.fetchall()]


def count_users() -> int:
    """Returns total user count."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS cnt FROM users")
        row = cursor.fetchone()
        return row['cnt'] if row else 0

