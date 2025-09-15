import requests
import csv
import time

# -------------------------
# CONFIG
# -------------------------
URL = "https://oddspedia.com/api/v1/getLeagues?topLeaguesOnly=1&includeLeaguesWithoutMatches=1&geoCode=BD&language=en"
SAVE_FILE = "odds_data.csv"
REQUEST_INTERVAL = 60   

# -------------------------
# FUNCTION: fetch data
# -------------------------
def fetch_data():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# -------------------------
# FUNCTION: save to CSV
# -------------------------
def save_to_csv(data, mode='w'):
    if not data:
        return
    odds_data = data.get("data", {})

    with open(SAVE_FILE, mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # header only if overwrite ('w' mode)
        if mode == 'w':
            writer.writerow(['ID', 'Name', 'Alt Name', 'Period', 'Way Type', 'Has Handicap', 'Payout', 'Options'])

        for key, item in odds_data.items():
            options = ", ".join(item.get('oddsnames', []))
            writer.writerow([
                item.get('id'),
                item.get('name'),
                item.get('alternative_name'),
                item.get('period'),
                item.get('waytype'),
                item.get('has_handicap'),
                item.get('payout'),
                options
            ])
    print(f"Data saved to {SAVE_FILE}")


while True:
    data = fetch_data()
    
    save_to_csv(data, mode='w')
    print("Waiting for next fetch...")
    time.sleep(REQUEST_INTERVAL)
