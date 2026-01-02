-- =========================
-- Public Price Tracker Schema
-- =========================

PRAGMA foreign_keys = ON;

-- ---------- DIMENSIONS ----------

CREATE TABLE IF NOT EXISTS dim_country (
  country_code TEXT PRIMARY KEY,
  country_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_commodity (
  commodity_code TEXT PRIMARY KEY,
  commodity_name TEXT NOT NULL,
  commodity_category TEXT
);

CREATE TABLE IF NOT EXISTS dim_market (
  market_code TEXT PRIMARY KEY,
  market_name TEXT NOT NULL,
  country_code TEXT NOT NULL,
  admin1_name TEXT,
  admin2_name TEXT,
  latitude REAL,
  longitude REAL,
  FOREIGN KEY (country_code) REFERENCES dim_country(country_code)
);

CREATE TABLE IF NOT EXISTS dim_date_month (
  month_id INTEGER PRIMARY KEY,         -- e.g., 202401
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,               -- 1-12
  month_start_date TEXT NOT NULL        -- 'YYYY-MM-01'
);

-- ---------- FACT ----------

CREATE TABLE IF NOT EXISTS fact_food_price_monthly (
  price_id INTEGER PRIMARY KEY AUTOINCREMENT,
  month_id INTEGER NOT NULL,
  market_code TEXT NOT NULL,
  commodity_code TEXT NOT NULL,
  price_type TEXT NOT NULL,             -- Retail only in this project
  currency_code TEXT,
  unit TEXT,
  price REAL NOT NULL,
  data_source TEXT NOT NULL DEFAULT 'WFP/HDX',
  FOREIGN KEY (month_id) REFERENCES dim_date_month(month_id),
  FOREIGN KEY (market_code) REFERENCES dim_market(market_code),
  FOREIGN KEY (commodity_code) REFERENCES dim_commodity(commodity_code)
);

-- Helpful indexes for performance (Power BI + SQL queries)
CREATE INDEX IF NOT EXISTS idx_fact_month ON fact_food_price_monthly(month_id);
CREATE INDEX IF NOT EXISTS idx_fact_market ON fact_food_price_monthly(market_code);
CREATE INDEX IF NOT EXISTS idx_fact_commodity ON fact_food_price_monthly(commodity_code);
