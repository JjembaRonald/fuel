-- Create fuel types lookup to enforce data integrity
CREATE TYPE fuel_category AS ENUM ('Petrol', 'Diesel', 'Kerosene');

--Table for scraped real-time pump prices from retailers
CREATE TABLE retailer_prices (
    price_id SERIAL PRIMARY KEY,
    station_name VARCHAR(50) NOT NULL, -- Shell, TotalEnergies, Stabex, Mogas
    location VARCHAR(50) NOT NULL,    -- Kampala, Gulu, Mbarara, etc.
    fuel_type fuel_category NOT NULL,
    pump_price_ugx DECIMAL(10, 2) NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

--Table for external global economic data feeds
CREATE TABLE economic_benchmarks (
    benchmark_id SERIAL PRIMARY KEY,
    brent_crude_usd_per_bbl DECIMAL(6, 2) NOT NULL,
    usd_ugx_exchange_rate DECIMAL(8, 2) NOT NULL,
    recorded_date DATE UNIQUE NOT NULL DEFAULT CURRENT_DATE
);

--Table for storing ML model prediction results
CREATE TABLE price_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    fuel_type fuel_category NOT NULL,
    predicted_price_ugx DECIMAL(10, 2) NOT NULL,
    mae_score DECIMAL(6, 2), -- Mean Absolute Error tracking
    forecast_for_date DATE NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for ultra-fast dashboard queries and filtering
CREATE INDEX idx_retailer_station ON retailer_prices(station_name, location);
CREATE INDEX idx_forecast_date ON price_forecasts(forecast_for_date);
