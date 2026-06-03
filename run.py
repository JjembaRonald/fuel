from scraping.engine import ingest_global_benchmarks, scrape_retailer_prices
import subprocess
import sys
import time


# Run the ingestion tasks
ingest_global_benchmarks()
scrape_retailer_prices()

def launch_system():
    print("Initializing National Fuel Pricing Regulation Ecosystem...")
    
    #Startup the FastAPI Web Service (Port 8000)
    api_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000"])
    
    # Give the backend API server a couple seconds to cleanly bind ports
    time.sleep(2)
    
    #Startup the Streamlit UI Dashboard Interface (Port 8501)
    try:
        print("Starting up interactive frontend layout engine...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard/app.py"], check=True)
    except KeyboardInterrupt:
        print("\nShutting down regulatory services safely...")
        api_process.terminate()

if __name__ == "__main__":
    launch_system()
