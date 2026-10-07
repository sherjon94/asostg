# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "gaybullaev").lstrip("@")
ADMIN_URL = f"https://t.me/{ADMIN_USERNAME}"
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) if os.getenv("ADMIN_ID", "").strip().isdigit() else 0
DONATE_URL = os.getenv("DONATE_URL", "https://taps.uz/shergaybullayev")


def is_admin(user) -> bool:
    if not user:
        return False
    if ADMIN_ID and user.id == ADMIN_ID:
        return True
    if user.username and user.username.lower() == ADMIN_USERNAME.lower():
        return True
    return False

# Path where sample files are stored on this machine
SAMPLE_FILES_DIR = Path(r"E:\п\2025\2026\др.файл")
SAMPLE_FILES = {
    "uz": SAMPLE_FILES_DIR / "uz.pdf",
    "ru": SAMPLE_FILES_DIR / "ru.pdf",
    "eng": SAMPLE_FILES_DIR / "eng.pdf",
    "ai": SAMPLE_FILES_DIR / "si.pdf",
}

# Supported languages
LANG_OPTIONS = {
    "uz-cyrl": "🇺🇿 Ўзбекча (Кирилл)",
    "uz-latn": "🇺🇿 Oʻzbekcha (Lotin)",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

STATUS_LABELS = {
    "tayanch": "Tayanch doktorant",
    "mustaqil": "Mustaqil izlanuvchi",
}

DEGREE_OPTIONS = [
    "фалсафа доктори (PhD) диссертацияси",
    "фан доктори (DSc) диссертацияси",
]
