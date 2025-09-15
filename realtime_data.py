import requests
import csv
import time

# ----------------------------
# CONFIG
# ----------------------------
url = "https://oddspedia.com/api/v1/getLeagueStandings?leagueId=1&season=131129&language=en"
headers = {
    "authority": "oddspedia.com",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "referer": "https://oddspedia.com/"
}
save_file = "league_standings.csv"
refresh_interval = 60  # seconds (change if needed)

# ----------------------------
# FUNCTION: fetch + save
# ----------------------------
def fetch_and_save():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Error:", response.status_code)
        return

    data = response.json()
    standings = data.get("data", {}).get("tables", [])[0].get("rows", [])

    with open(save_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Team", "Played", "Wins", "Draws", "Losses", "Goals", "Points"])

        for row in standings:
            team = row.get("team", {}).get("name", "")
            writer.writerow([
                row.get("pos"),          # Rank
                team,                   # Team name
                row.get("played"),      # Matches played
                row.get("wins"),        # Wins
                row.get("draws"),       # Draws
                row.get("losses"),      # Losses
                row.get("goals"),       # Goals (e.g. 10:5)
                row.get("points")       # Points
            ])

    print(f"✅ Updated: {save_file}")

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    fetch_and_save()
    print(f"⏳ Waiting {refresh_interval} sec...")
    time.sleep(refresh_interval)
