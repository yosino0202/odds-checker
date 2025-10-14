import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://race.netkeiba.com"

def get_today_race_list():
    """今日のレース一覧取得"""
    url = f"{BASE_URL}/top/"
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    races = []
    for a in soup.select("a[href*='race_id=']"):
        href = a.get("href")
        if "odds" in href and "index.html" in href:
            race_url = href if href.startswith("http") else BASE_URL + href
            race_name = a.text.strip()
            if race_name and race_url not in [r["url"] for r in races]:
                races.append({"name": race_name, "url": race_url})
    return races

def get_predicted_odds(race_url):
    res = requests.get(race_url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    horses, odds = [], []
    for tr in soup.select("table tbody tr"):
        name_tag = tr.select_one("td.Horse_Name a")
        odds_tag = tr.select_one("td.Odds")
        if name_tag and odds_tag:
            horses.append(name_tag.text.strip())
            try:
                odds.append(float(odds_tag.text.strip()))
            except:
                odds.append(None)

    df = pd.DataFrame({"馬名": horses, "予想オッズ": odds})
    df["勝率(予想)"] = 1 / df["予想オッズ"]
    df["勝率(予想)"] = df["勝率(予想)"].fillna(0)
    return df

def get_actual_odds(race_url):
    res = requests.get(race_url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    horses, odds = [], []
    for tr in soup.select("table tbody tr"):
        name_tag = tr.select_one("td.Horse_Name a")
        odds_tag = tr.select_one("td.Odds")
        if name_tag and odds_tag:
            horses.append(name_tag.text.strip())
            try:
                odds.append(float(odds_tag.text.strip()))
            except:
                odds.append(None)

    df = pd.DataFrame({"馬名": horses, "実オッズ": odds})
    return df