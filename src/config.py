# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# ─── 1) Project Root ─────────────────────────────────────────────────────────────
# This file lives in <project>/src, so one parent up is the repo root.
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# ─── 2) Load the “real” .env from the repo root ──────────────────────────────────
load_dotenv(PROJECT_ROOT / ".env")

# ─── 3) Helpers ─────────────────────────────────────────────────────────────────
def _env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val

def _env_path(name: str, fallback: Path) -> Path:
    raw = os.getenv(name)
    return Path(raw).expanduser().resolve() if raw else fallback.resolve()

# ─── 4) Secrets & Tokens ─────────────────────────────────────────────────────────
GEMINI_API         = _env("GEMINI_API")
JSON_API           = _env("JSON_API")
CX                 = _env("CX")
IG_USERNAME        = _env("IG_USERNAME")
IG_PASSWORD        = _env("IG_PASSWORD")
TELEGRAM_BOT_TOKEN = _env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = _env("TELEGRAM_CHAT_ID")

# ─── 5) Session file ──────────────────────────────────────────────────────────────
# Default to your Windows home if SESSION_FILE isn’t set.
SESSION_FILE = _env_path("SESSION_FILE", Path.home() / "session.json")

# ─── 6) Temp download dir ─────────────────────────────────────────────────────────
TEMP_DOWNLOAD_PATH = Path(
    os.getenv("TEMP_DOWNLOAD_PATH", PROJECT_ROOT / "temp_down")
).expanduser().resolve()

# ─── 7) Debug flag ────────────────────────────────────────────────────────────────
DEBUG_MODE = False

# ─── 8) Google Search ─────────────────────────────────────────────────────────────
TOPIC_LIST = [
    "memes", "dank memes", "humorous memes", "brainrot memes", "normie memes", "classic memes",
    "reddit memes", "dark memes", "iphone memes", "twitter memes", "wholesome memes",
    "relatable memes", "surreal memes", "video memes", "vine memes", "facebook memes",
    "instagram memes", "tiktok memes", "political memes", "animal memes", "gaming memes",
    "reaction memes", "wojak memes", "pepe memes", "spoof memes", "educational memes",
    "anime memes", "spongebob memes", "historical memes", "office memes", "work memes",
    "student memes", "programmer memes", "engineering memes", "sports memes", "music memes",
    "movie memes", "tv show memes", "caption memes", "baby yoda memes", "cat memes", "dog memes",
    "food memes", "fitness memes", "relationship memes", "parenting memes", "school memes",
    "celebrity memes", "tech memes", "travel memes", "art memes", "book memes", "science memes",
    "math memes", "physics memes", "chemistry memes", "biology memes", "medical memes", "law memes",
    "finance memes", "economics memes", "marketing memes", "business memes", "startup memes",
    "coding memes", "data science memes", "AI memes", "machine learning memes", "robotics memes",
    "space memes", "astronomy memes", "weather memes", "holiday memes", "vacation memes",
    "city memes", "country memes", "language memes", "cultural memes", "history memes",
    "psychology memes", "sociology memes", "politics memes", "environmental memes",
    "green energy memes", "eco-friendly memes", "nature memes", "wildlife memes",
    "conservation memes", "funny animal memes", "weird memes", "absurd memes", "ironic memes",
    "sarcastic memes", "pun memes", "wordplay memes", "funniest memes of all time",
    "most popular memes", "viral memes", "trending memes", "new memes", "latest memes",
    "hilarious memes", "best memes", "epic memes", "best memes of 2023", "best memes of 2024",
    "best memes of 2025", "make me laugh memes", "comedy memes", "silly memes", "goofy memes",
    "quirky memes", "witty memes", "clever memes", "smart memes", "intelligent memes",
    "absurdist memes", "existential memes", "nihilistic memes", "dark humor memes",
    "black humor memes", "brainy memes", "intellectual memes", "nerdy memes", "geeky memes",
    "dorky memes", "awkward memes"
]
