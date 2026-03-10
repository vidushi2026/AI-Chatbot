import json
import os
import random

def run_scraper(simulate_change=False):
    """
    Simulated scraper that updates the local data.
    In a production environment, this would hit Groww.in using BeautifulSoup/Selenium.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'ingested_data.json')
    
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        if simulate_change:
            # Simulate a small change in expense ratio or timestamp
            # to verify the scheduler detects a hash change
            if "funds" in data and len(data["funds"]) > 0:
                fund = data["funds"][0]
                fund["expense_ratio"] = f"{random.uniform(0.1, 1.0):.2f}%"
                print(f"Simulated data update for: {fund['name']}")
    
        with open(data_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Scraper run complete. Data saved to {data_path}")
    else:
        print("Scraper Error: ingested_data.json not found.")

if __name__ == "__main__":
    import sys
    simulate = "--simulate" in sys.argv
    run_scraper(simulate_change=simulate)
