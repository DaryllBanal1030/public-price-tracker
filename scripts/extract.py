# scripts/extract.py
import base64
from io import StringIO
import pandas as pd
import requests

from config import (
    RAW_DIR,
    HAPI_BASE_URL,
    FOOD_PRICES_ENDPOINT,
    APP_NAME,
    EMAIL,
    COUNTRIES,
    COMMODITIES,
    PRICE_TYPE,
    START_YEAR,
    END_YEAR,
    RAW_OUTPUT_FILENAME,
)

LIMIT = 10000  # API returns up to 10,000 rows per response :contentReference[oaicite:2]{index=2}


def make_app_identifier(app_name: str, email: str) -> str:
    raw = f"{app_name}:{email}".encode("utf-8")
    return base64.b64encode(raw).decode("utf-8")


def fetch_all(params: dict) -> pd.DataFrame:
    """Fetch all pages for a given param set, return as one DataFrame."""
    all_rows = []
    offset = 0

    while True:
        page_params = params | {"limit": LIMIT, "offset": offset, "output_format": "json"}
        url = f"{HAPI_BASE_URL}{FOOD_PRICES_ENDPOINT}"

        r = requests.get(url, params=page_params, timeout=60)
        r.raise_for_status()

        payload = r.json()
        rows = payload.get("data", payload)  # some endpoints return {data:[...]}
        if not rows:
            break

        all_rows.extend(rows)

        # If we got fewer than LIMIT, we're done
        if len(rows) < LIMIT:
            break

        offset += LIMIT

    return pd.DataFrame(all_rows)


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    app_identifier = make_app_identifier(APP_NAME, EMAIL)

    # Build one combined dataset by looping through (country, commodity)
    frames = []
    for country in COUNTRIES:
        for commodity in COMMODITIES:
            params = {
                "app_identifier": app_identifier,
                "location_code": country,
                "commodity_name": commodity,
                "price_type": PRICE_TYPE,
                # Keep the window tight (monthly series)
                "reference_period_start_min": f"{START_YEAR}-01-01",
                "reference_period_start_max": f"{END_YEAR}-12-31",
            }
            df_part = fetch_all(params)
            if not df_part.empty:
                frames.append(df_part)

    if not frames:
        print("No rows returned. Check commodity names / filters.")
        return 1

    df = pd.concat(frames, ignore_index=True)

    # Keep only columns we care about (safe even if extras exist)
    keep_cols = [
        "commodity_code", "commodity_name", "commodity_category",
        "price_type", "price", "unit", "currency_code",
        "reference_period_start", "reference_period_end",
        "location_code", "location_name",
        "admin1_code", "admin1_name",
        "admin2_code", "admin2_name",
        "market_code", "market_name",
        "lat", "lon",
        "resource_hdx_id",
    ]
    existing = [c for c in keep_cols if c in df.columns]
    df = df[existing].copy()

    out_path = RAW_DIR / RAW_OUTPUT_FILENAME
    df.to_csv(out_path, index=False)

    print(f"Saved filtered raw data: {out_path}")
    print(f"Rows saved: {len(df):,}")
    print(f"Countries: {COUNTRIES}")
    print(f"Commodities: {COMMODITIES}")
    print(f"Price type: {PRICE_TYPE}")
    print(f"Years: {START_YEAR} to {END_YEAR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
