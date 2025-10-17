import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper import fetch_predicted_odds
from utils import odds_to_probability, calculate_expectation

st.title("🐎 netkeiba オッズ期待値チェッカー")

# 予想オッズ取得
if st.button("🔁 全レースの予想オッズを取得"):
    with st.spinner("netkeibaから予想オッズを取得中..."):
        races = fetch_predicted_odds()
        st.success(f"{len(races)}件のレースを取得しました！")

# CSV読み込み
try:
    df = pd.read_csv("data/races.csv")
    st.dataframe(df)
except FileNotFoundError:
    st.warning("まだレース情報が取得されていません。上のボタンを押してください。")

# 勝率変換デモ
st.subheader("🎯 オッズ → 勝率変換テスト")
input_odds = st.number_input("オッズを入力", min_value=1.0, value=2.5, step=0.1)
prob = odds_to_probability(input_odds)
st.write(f"→ 勝率: **{prob * 100:.1f}%**")