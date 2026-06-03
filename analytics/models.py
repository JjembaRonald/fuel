import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from config.database import db

# Uganda Government regulated pricing constants
URA_EXCISE_DUTY_PETROL = 1450.00   # UGX per liter fixed tax
URA_EXCISE_DUTY_DIESEL = 1130.00   # UGX per liter fixed tax
TRANSPORT_LOGISTICS_COST = 480.00  # Pipeline/trucking from Mombasa per liter
MAX_ALLOWED_PROFIT_MARGIN = 0.08  # Government statutory cap (8% max OMC profit)

def calculate_regulated_ceiling(brent_crude_usd, exchange_rate, fuel_type):
    """
    Applies the official regulatory formula to determine the absolute maximum
    legal pump price allowed for a retail station.
    """
    # 1 Barrel = 158.98 Liters
    crude_per_liter_usd = float(brent_crude_usd) / 158.98
    crude_per_liter_ugx = crude_per_liter_usd * float(exchange_rate)
    
    # Apply matching tax policy based on the fuel type
    tax = URA_EXCISE_DUTY_PETROL if fuel_type == "Petrol" else URA_EXCISE_DUTY_DIESEL
    
    # Baseline landed cost before corporate profit markup
    landed_cost_ugx = (crude_per_liter_ugx + tax + TRANSPORT_LOGISTICS_COST)
    
    # Calculate final ceiling with the protected statutory profit margin cap
    max_retail_price = landed_cost_ugx * (1 + MAX_ALLOWED_PROFIT_MARGIN)
    return round(max_retail_price, 2)

def train_and_forecast_prices():
    """
    Extracts historical tracking parameters from the DB, trains a Linear 
    Regression forecasting model, and outputs the next-day price forecast.
    """
    try:
        # 1. Fetch historical benchmarks and retail averages from the DB to form a training dataset
        with db.get_cursor() as cursor:

            query = """
                SELECT b.brent_crude_usd_per_bbl, b.usd_ugx_exchange_rate, r.fuel_type, r.pump_price_ugx
                FROM economic_benchmarks b
                JOIN retailer_prices r ON r.scraped_at::date = b.recorded_date;
            """
            cursor.execute(query)
            records = cursor.fetchall()

        if not records or len(records) < 5:
            #If the database is fresh, it would have less than 5 records for training,
            #we inject synthetic variations based on current data to initialize your ML pipeline instantly.
            print(" Cold start: Simulating training variants to prime the ML algorithm...")
            training_data = []
            for f_type in ["Petrol", "Diesel"]:
                for i in range(1, 10):
                    base_crude = 75.0 + i
                    base_fx = 3780.0 + (i * 5)
                    calc_p = calculate_regulated_ceiling(base_crude, base_fx, f_type) - (i * 10)
                    training_data.append({
                        "brent_crude_usd_per_bbl": base_crude,
                        "usd_ugx_exchange_rate": base_fx,
                        "fuel_type": f_type,
                        "pump_price_ugx": calc_p
                    })
            df = pd.DataFrame(training_data)
        else:
            df = pd.DataFrame(records)

        #Process forecasts for each fuel category
        for fuel_category in ["Petrol", "Diesel"]:
            df_subset = df[df["fuel_type"] == fuel_category]
            
            if df_subset.empty:
                continue

            # Features (X) and Target (y)
            X = df_subset[["brent_crude_usd_per_bbl", "usd_ugx_exchange_rate"]]
            y = df_subset["pump_price_ugx"]

            # Train my system's core linear model
            model = LinearRegression()
            model.fit(X, y)

            # Evaluate system accuracy using Mean Absolute Error (MAE)
            predictions = model.predict(X)
            mae = mean_absolute_error(y, predictions)

            #Pull today's active metrics to build tomorrow's system forecast
            with db.get_cursor() as cursor:
                cursor.execute("SELECT brent_crude_usd_per_bbl, usd_ugx_exchange_rate FROM economic_benchmarks ORDER BY recorded_date DESC LIMIT 1;")
                latest_eco = cursor.fetchone()

            if latest_eco:
                current_crude = float(latest_eco["brent_crude_usd_per_bbl"])
                current_fx = float(latest_eco["usd_ugx_exchange_rate"])
            else:
                current_crude, current_fx = 78.50, 3780.00 # Standard system fallbacks

            #Run predictive model inference
            live_features = pd.DataFrame([[current_crude, current_fx]], columns=["brent_crude_usd_per_bbl", "usd_ugx_exchange_rate"])
            predicted_market_price = float(model.predict(live_features)[0])

            #Cross-verify forecast against regulatory policies to prevent market manipulation
            allowed_ceiling = calculate_regulated_ceiling(current_crude, current_fx, fuel_category)
            
            #Enforcing the ceiling, predicted public price cannot breach maximum allowed rates
            final_safe_forecast = min(predicted_market_price, allowed_ceiling)

            #Save the calculated forecast into your system database
            with db.get_cursor() as cursor:
                insert_query = """
                    INSERT INTO price_forecasts (fuel_type, predicted_price_ugx, mae_score, forecast_for_date)
                    VALUES (%s, %s, %s, CURRENT_DATE + INTERVAL '1 day');
                """
                cursor.execute(insert_query, (fuel_category, round(final_safe_forecast, 2), round(mae, 2)))

        print(" System ML Pipeline successfully executed. Forecasts calculated and saved.")
        return True

    except Exception as e:
        print(f"Error inside the price engine: {str(e)}")
        return False
