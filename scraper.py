import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 保存先ディレクトリ作成
os.makedirs("data", exist_ok=True)

def fetch_predicted_odds():
    """
    netkeibaの予想オッズをスクレイピングしてCSV化する
    """
    print("🔍 netkeibaから予想オッズを取得中...")

    base_url = "https://race.netkeiba.com/race/odds.html?race_id="
    race_ids = [
        # テスト用：今日のいくつかのレースID（毎日変わるので、動作確認後に自動化）
        "202405030811", "202405030812", "202405030813"
    ]

    all_data = []

    for race_id in race_ids:
        url = f"{base_url}{race_id}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        res.encoding = res.apparent_encoding

        if res.status_code != 200:
            print(f"❌ {race_id} の取得に失敗: {res.status_code}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        # 馬名と予想オッズを取得
        rows = soup.select("table.odds_tan tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            uma_num = cols[0].get_text(strip=True)
            uma_name = cols[1].get_text(strip=True)
            odds_text = cols[2].get_text(strip=True).replace("倍", "")

            try:
                odds = float(odds_text)
                win_prob = round(100 / odds, 2)  # 勝率に変換
            except ValueError:
                odds, win_prob = None, None

            all_data.append({
                "race_id": race_id,
                "馬番": uma_num,
                "馬名": uma_name,
                "予想オッズ": odds,
                "予想勝率(%)": win_prob,
            })

    if not all_data:
        print("⚠️ データを取得できませんでした。")
        return None

    df = pd.DataFrame(all_data)
    df["取得日時"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv("data/races.csv", index=False, encoding="utf-8-sig")
    print("✅ races.csv を更新しました。")

    return df


if __name__ == "__main__":
    fetch_predicted_odds()