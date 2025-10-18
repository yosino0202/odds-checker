import streamlit as st
import pandas as pd
import os
from scraper import fetch_predicted_odds

st.set_page_config(page_title="netkeiba オッズ比較ツール", layout="wide")

st.title("🐎 netkeiba オッズ比較ツール（自動更新対応）")

# --- CSVファイル or スクレイピングからデータ取得 ---
csv_path = "data/races.csv"

# ファイルがあるか確認
if os.path.exists(csv_path):
    try:
        df = pd.read_csv(csv_path)
        st.success(f"📊 保存済みデータを読み込みました（{len(df)}件）")
    except Exception as e:
        st.warning(f"⚠️ CSVの読み込みに失敗しました: {e}")
        df = None
else:
    st.info("🔍 races.csv が見つかりません。scraper.py から取得します...")
    df = fetch_predicted_odds()

# --- データ表示またはメッセージ ---
if df is None or len(df) == 0:
    st.warning("⚠️ データを取得できませんでした。GitHub Actions の自動更新を待ってください。")
else:
    st.success(f"✅ {len(df)} 件のレースデータを表示中！")
    st.dataframe(df, use_container_width=True)

# --- 説明セクション ---
st.divider()
st.caption("""
このアプリは GitHub Actions により自動で netkeiba の予想オッズを取得し、
最新データを表示します。
""")