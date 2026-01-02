# scripts/config.py
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DB_PATH = PROJECT_ROOT / "prices.db"

# ---- HDX HAPI API v2 ----
HAPI_BASE_URL = "https://hapi.humdata.org/api/v2"
FOOD_PRICES_ENDPOINT = "/food-security-nutrition-poverty/food-prices-market-monitor"

# app_identifier requirement (base64 of "app_name:email") :contentReference[oaicite:1]{index=1}
APP_NAME = "public-price-tracker"
EMAIL = "darylllbanal@gmail.com"  # <- change this

# ---- Scope (locked) ----
COUNTRIES = ["PHL", "VNM", "IDN"]
COMMODITIES = ["Rice", "Cooking Oil", "Sugar", "Eggs"]
PRICE_TYPE = "Retail"

# ---- Time window (last 5 years) ----
END_YEAR = date.today().year
START_YEAR = END_YEAR - 4

RAW_OUTPUT_FILENAME = "food_prices_raw_filtered.csv"
