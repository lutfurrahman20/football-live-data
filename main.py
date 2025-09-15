import requests
import time
import json
from datetime import datetime

url = "https://iscjxxqgmb.com/api/v1/allsports/sports?ss=all&ltr=0"  

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

def fetch_data():
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        
        output = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }

        
        with open("sports_data.json", "a", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False)
            f.write("\n")  

        print("✅ Data saved at", output["timestamp"])

       
        for sport in data:
            print(f"{sport['title']} → Live: {sport['count_live']}, Pregame: {sport['count_pregame']}")

    except Exception as e:
        print("❌ Error fetching data:", e)


if __name__ == "__main__":
    while True:
        fetch_data()
        time.sleep(10)   
