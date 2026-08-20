import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

BTC_ADDRESS = os.getenv("BTC_ADDRESS", "bc1q4xr3k7ygeyc7s8nmt0ek4gdcelp6emfudtv99u")
ETH_USDT_ADDRESS = os.getenv("ETH_USDT_ADDRESS", "0xfe94ddcc4799199cea5c4debb0e9d2ebfb7c813d").lower()
USDT_CONTRACT = os.getenv("USDT_CONTRACT", "0xdAC17F958D2ee523a2206206994597C13D831ec7").lower()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
DOWNLOAD_TTL_SECONDS = int(os.getenv("DOWNLOAD_TTL_SECONDS", "3600"))
DOWNLOAD_SECRET = os.getenv("DOWNLOAD_SECRET", "change-me-to-a-long-random-string")
FILES_DIR = Path(os.getenv("FILES_DIR", str(BASE_DIR / "files")))
DATA_DIR = BASE_DIR / "data"
ORDERS_FILE = DATA_DIR / "orders.json"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))

PRODUCTS = {
    "canvas": {"name": "Content Scarcity Canvas", "price_usd": 29.0, "file": "canvas.pdf"},
    "playbook": {"name": "Scarcity Playbook", "price_usd": 79.0, "file": "playbook.pdf"},
    "bundle": {"name": "Complete Scarcity Bundle", "price_usd": 129.0, "file": "bundle.zip"},
    "checklist": {"name": "Content Scarcity Checklist", "price_usd": 19.0, "file": "checklist.pdf"},
    "templates": {"name": "Scarcity Message Templates", "price_usd": 39.0, "file": "templates.pdf"},
    "decision-tool": {"name": "Scarcity Decision Tool", "price_usd": 49.0, "file": "decision-tool.pdf"},
}

AMOUNT_TOLERANCE_USD = 1.0
