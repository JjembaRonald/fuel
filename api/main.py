from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from config.database import db

#Initialize FastAPI with auto-generated documentation metadata
app = FastAPI(
    title="National Fuel Pricing Regulation API",
    description="Government regulatory endpoint tracking retail violations, global economic vectors, and ML price caps.",
    version="1.0.0"
)

# Enforce secure CORS policy configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific URLs in a production cluster
    allow_credentials=True,
    allow_methods=["GET"], # Limit system access strictly to data reads
    allow_headers=["*"],
)

@app.get("/")
async def root():
    # System Health Check endpoint.
    return {"status": "operational", "system": "Uganda Fuel Regulatory Backend"}


@app.get("/api/v1/market-overview")
async def get_market_overview():
    """
    Fetches the latest real-time scraped retail pump matrix 
    across all tracked regional energy hubs.
    """
    try:
        with db.get_cursor() as cursor:
            query = """
                SELECT price_id, station_name, location, fuel_type, pump_price_ugx, scraped_at
                FROM retailer_prices
                ORDER BY scraped_at DESC LIMIT 20;
            """
            cursor.execute(query)
            records = cursor.fetchall()
            return {"count": len(records), "data": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database retrieval failure: {str(e)}")


@app.get("/api/v1/regulatory-caps")
async def get_regulatory_caps():
    """
    Exposes the latest global economic metrics along with calculated tomorrow ready 
    machine learning price forecasts and legal maximum regulatory bounds.
    """
    try:
        with db.get_cursor() as cursor:
            query = """
                SELECT DISTINCT ON (fuel_type) forecast_id, fuel_type, predicted_price_ugx, mae_score, forecast_for_date, generated_at
                FROM price_forecasts
                ORDER BY fuel_type, forecast_for_date DESC;
            """
            cursor.execute(query)
            forecasts = cursor.fetchall()
            
            #Fetch latest baseline economic indicators
            cursor.execute("SELECT brent_crude_usd_per_bbl, usd_ugx_exchange_rate, recorded_date " \
                            "FROM economic_benchmarks ORDER BY recorded_date DESC LIMIT 1;")
            benchmarks = cursor.fetchone()
            
            return {
                "economic_indicators": benchmarks if benchmarks else {},
                "regulatory_forecast_caps": forecasts
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database retrieval failure: {str(e)}")


@app.get("/api/v1/compliance-audit")
async def audit_market_compliance(station: str = Query(None, description="Filter audit logs by retail name")):
    """
    Performs a real-time regulatory compliance audit. Flags any retail stations
    selling fuel above the system's machine learning model forecast cap.
    """
    try:
        with db.get_cursor() as cursor:
            #Query cross references active pump pricing against active daily forecast ceilings
            query = """
                SELECT r.price_id, r.station_name, r.location, r.fuel_type, r.pump_price_ugx AS active_pump_price,
                       f.predicted_price_ugx AS maximum_legal_cap,
                       (r.pump_price_ugx - f.predicted_price_ugx) AS violation_margin_ugx,
                       CASE WHEN r.pump_price_ugx > f.predicted_price_ugx THEN 'VIOLATION' ELSE 'COMPLIANT' END AS compliance_status
                FROM retailer_prices r
                JOIN price_forecasts f ON r.fuel_type = f.fuel_type AND f.forecast_for_date = CURRENT_DATE
                WHERE (%s IS NULL OR r.station_name ILIKE %s)
                ORDER BY violation_margin_ugx DESC;
            """
            cursor.execute(query, (station, station))
            audit_logs = cursor.fetchall()
            
            violations_count = sum(1 for log in audit_logs if log["compliance_status"] == "VIOLATION")
            
            return {
                "audit_date": str(date.today()),
                "total_monitored": len(audit_logs),
                "total_violations_detected": violations_count,
                "audit_results": audit_logs
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance processing failure: {str(e)}")
