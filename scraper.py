import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

# dataフォルダがなければ自動作成
os.makedirs("data", exist_ok=True)

def fetch_predicted_odds():
    """
    netkeibaの予想オッズを自動取得
    データが取れなかった場合はダミーデータで補う
    """
    base_url = "https://race.netkeiba.com"
    odds_top_url = f"{base_url}/top/odds_list.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_data = []

    try:
        response = requests.get(odds_top_url, headers=headers, timeout=10)
        response.encoding = "EUC-JP"
        soup = BeautifulSoup(response.text, "html.parser")

        race_links = []
        for a in soup.select("a[href*='odds/index.html?race_id=']"):
            href = a.get("href")
            if "race_id=" in href:
                race_links.append(base_url + href)

        for link in race_links[:5]:  # 通信節約
            race_id = re.search(r"race_id=(\d+)", link).group(1)
            race_name = f"Race {race_id}"
            r = requests.get(link, headers=headers, timeout=10)
            r.encoding = "EUC-JP"
            s = BeautifulSoup(r.text, "html.parser")

            horses = [t.get_text(strip=True) for t in s.select(".HorseName a")]
            odds = [t.get_text(strip=True) for t in s.select(".Odds span")]

            for name, odd in zip(horses, odds):
                try:
                    all_data.append({
                        "race": race_name,
                        "horse": name,
                        "predicted_odds": float(odd)
                    })
                except ValueError:
                    continue

    except Exception as e:
        print("Error during scraping:", e)

    # 🧩 もしデータが空なら、ダミーデータを入れる
    if not all_data:
        all_data = [
            {"race": "東京11R", "horse": "サンプルホースA", "predicted_odds": 2.8},
            {"race": "東京11R", "horse": "サンプルホースB", "predicted_odds": 4.2},
            {"race": "京都10R", "horse": "サンプルホースC", "predicted_odds": 5.5},
        ]

    df = pd.DataFrame(all_data)
    df.to_csv("data/races.csv", index=False)
    return df