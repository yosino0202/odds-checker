import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 💡 dataフォルダがなければ自動で作成
os.makedirs("data", exist_ok=True)

def fetch_predicted_odds():
    """
    netkeibaの予想オッズを取得する代わりに、
    まずはアプリ全体の動作確認用にダミーデータを生成します。
    """
    
    # ▼テスト用のサンプルデータ（後で実データに差し替え可能）
    data = [
        {"race": "東京11R", "horse": "サンプルホースA", "predicted_odds": 2.8},
        {"race": "東京11R", "horse": "サンプルホースB", "predicted_odds": 4.2},
        {"race": "東京11R", "horse": "サンプルホースC", "predicted_odds": 7.6},
        {"race": "京都10R", "horse": "サンプルホースD", "predicted_odds": 3.5},
        {"race": "京都10R", "horse": "サンプルホースE", "predicted_odds": 5.8},
    ]
    
    # ▼DataFrame化
    df = pd.DataFrame(data)
    
    # ▼ローカルにCSVとして保存（Streamlit Cloud上でもOK）
    df.to_csv("data/races.csv", index=False)
    
    return df