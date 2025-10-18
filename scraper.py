import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 💡 追加：dataフォルダがなければ自動で作成
os.makedirs("data", exist_ok=True)

def fetch_predicted_odds():
    url = "https://race.netkeiba.com/odds/index.html"
    # ... ここから下はあなたの元の処理そのままでOK
    # 取得 → DataFrame化 → CSV保存
    df = pd.DataFrame([...])
    df.to_csv("data/races.csv", index=False)
    return df