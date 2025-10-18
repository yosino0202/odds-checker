import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 💡 dataフォルダがなければ自動で作成
os.makedirs("data", exist_ok=True)

def fetch_predicted_odds():
    # 本来は netkeiba から取得するけど、まずはテスト用データで動作確認
    data = [
        {"race": "東京11R", "horse": "サンプルホースA", "predicted_odds": 2.8},
        {"race": "東京11R", "horse": "サンプルホースB", "predicted_odds": 4.2},
        {"race": "東京11R", "horse": "サンプルホースC", "predicted_odds": 7.6},
    ]
    
    df = pd.DataFrame(data)
    df.to_csv("data/races.csv", index=False)
    return df