import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

# dataフォルダがなければ自動作成
os.makedirs("data", exist_ok=True)

def fetch_predicted_odds():
    """
    netkeibaの全開催レースの予想オッズを自動で取得してCSV保存
    """
    base_url = "https://race.netkeiba.com"
    odds_top_url = f"{base_url}/top/odds_list.html"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(odds_top_url, headers=headers)
    response.encoding = "EUC-JP"
    soup = BeautifulSoup(response.text, "html.parser")

    # 各レースページのリンク取得
    race_links = []
    for a in soup.select("a[href*='odds/index.html?race_id=']"):
        href = a.get("href")
        if "race_id=" in href:
            race_links.append(base_url + href)

    all_data = []

    for link in race_links[:10]:  # 通信量を抑えるため10レースまで
        race_id = re.search(r"race_id=(\d+)", link).group(1)
        race_name = f"Race {race_id}"

        try:
            r = requests.get(link, headers=headers)
            r.encoding = "EUC-JP"
            s = BeautifulSoup(r.text, "html.parser")

            # 馬名と予想オッズを取得
            horses = [t.get_text(strip=True) for t in s.select(".HorseList .HorseName a")]
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
        except Exception:
            continue

    # DataFrameに変換
    df = pd.DataFrame(all_data)

    # CSV保存
    df.to_csv("data/races.csv", index=False)

    return df