import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_predicted_odds():
    """netkeibaの予想オッズ一覧をスクレイピング"""
    url = "https://race.netkeiba.com/odds/index.html"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    races = []
    # 仮のデータ構造（実際はHTML構造に合わせて調整）
    for race in soup.select(".RaceList_Box a"):
        race_name = race.text.strip()
        race_url = race.get("href")
        races.append({
            "レース名": race_name,
            "URL": f"https://race.netkeiba.com{race_url}"
        })
    
    df = pd.DataFrame(races)
    df.to_csv("data/races.csv", index=False)
    return df