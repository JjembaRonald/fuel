import os
import requests
from config.database import db

EIA_API_KEY = os.getenv("EIA_API_KEY")


def ingest_global_benchmarks():
    """Fetches real-time Brent Crude data and logs local USD/UGX rates."""
    
    url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

    #query string keys from the EIA URL(browser)
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "weekly",
        "data[0]": "value",
        "facets[series][]": "RBRTE",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 5000,  
    }

    try:
        #Fetch Global Crude Price
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        eia_data = response.json()

        # Dig straight into the data array inside response
        data_list = eia_data.get("response", {}).get("data", [])

        if not data_list:
            print("Error: No data records returned from EIA API.")
            return False

        latest_record = data_list[0]
        brent_crude = float(latest_record["value"])


        #Fetch Latest USD to UGX exchange rate via Open Exchange Rates (or fallback)
        #this is has a trial period of 2 weeks so i will implement it later incase am to showcase my project
        usd_ugx = 3780.00
        try:
            fx_res = requests.get(
                "https://er-api.com", timeout=5
            )
            if fx_res.status_code == 200:
                usd_ugx = float(fx_res.json()["rates"].get("UGX", 3780.00))
        except Exception:
            pass  # Fallback to base rate if FX API is congested

        #Save to database using my secure DB manager
        with db.get_cursor() as cursor:
            query = """
                INSERT INTO economic_benchmarks (brent_crude_usd_per_bbl, usd_ugx_exchange_rate, recorded_date)
                VALUES (%s, %s, CURRENT_DATE)
                ON CONFLICT (recorded_date) DO UPDATE 
                SET brent_crude_usd_per_bbl = EXCLUDED.brent_crude_usd_per_bbl,
                    usd_ugx_exchange_rate = EXCLUDED.usd_ugx_exchange_rate;
            """
            cursor.execute(query, (brent_crude, usd_ugx))

        print(
            f" Successfully logged Economic Data: Brent Crude ${brent_crude}/bbl | FX: {usd_ugx} UGX"
        )
        return True

    except Exception as e:
        print(f"Error during global benchmark ingestion: {str(e)}")
        return False


def scrape_retailer_prices():
    """Simulating localized scraping extraction across Ugandan fuel hubs.

    Since Ugandan OMCs dynamically protect active pump APIs, this parses
    and validates operational pricing matrices for system testing.
    """
    # Sample matrix mimicking regional distribution centers (Kampala Central, Mbarara, Gulu)
    simulated_scraped_data = [
        {"station": "Shell", "loc": "Kampala", "type": "Petrol", "price": 5410.00},
        {"station": "Shell", "loc": "Kampala", "type": "Diesel", "price": 5280.00},
        {"station": "TotalEnergies", "loc": "Kampala", "type": "Petrol", "price": 5390.00},
        {"station": "TotalEnergies", "loc": "Kampala", "type": "Diesel", "price": 5290.00},
        {"station": "Stabex", "loc": "Mbarara", "type": "Petrol", "price": 5460.00},
        {"station": "Stabex", "loc": "Mbarara", "type": "Diesel", "price": 5320.00},
        {"station": "Mogas", "loc": "Gulu", "type": "Petrol", "price": 5580.00},
        {"station": "Mogas", "loc": "Gulu", "type": "Diesel", "price": 5310.00},
        {"station": "Shell", "loc": "Kampala", "type": "Petrol", "price": 5510.00},
        {"station": "Shell", "loc": "Kampala", "type": "Diesel", "price": 5480.00},
        {"station": "TotalEnergies", "loc": "Kampala", "type": "Petrol", "price": 5690.00},
        {"station": "TotalEnergies", "loc": "Kampala", "type": "Diesel", "price": 5450.00},
        {"station": "Stabex", "loc": "Mbarara", "type": "Diesel", "price": 5220.00},
        {"station": "Stabex", "loc": "Mbarara", "type": "Petrol", "price": 5390.00},
        {"station": "Mogas", "loc": "Gulu", "type": "Diesel", "price": 5280.00},
        {"station": "Mogas", "loc": "Gulu", "type": "Petrol", "price": 5560.00},
    ]

    try:
        with db.get_cursor() as cursor:
            query = """
                INSERT INTO retailer_prices (station_name, location, fuel_type, pump_price_ugx)
                VALUES (%s, %s, %s, %s);
            """
            for row in simulated_scraped_data:
                cursor.execute(
                    query,
                    (
                        row["station"],
                        row["loc"],
                        row["type"],
                        row["price"],
                    ),
                )

        print(
            f" Successfully parsed and logged {len(simulated_scraped_data)} retail pump updates into the DB."
        )
        return True
    except Exception as e:
        print(f"Error during retail market logging: {str(e)}")
        return False
