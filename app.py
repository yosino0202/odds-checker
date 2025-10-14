import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from scraper import get_today_race_list, get_predicted_odds, get_actual_odds

# ページ設定
st.set_page_config(page_title="netkeiba予想オッズ期待値チェッカー", layout="wide")

st.title("🏇 netkeiba予想オッズ 期待値チェッカー")
st.write("このアプリは netkeiba の『予想オッズ』を自動取得し、実際のオッズと比較して期待値を表示します。")
st.write("💡 期待値1.0以上は赤文字でハイライト表示され、グラフで推移も確認できます。")

# --- 今日のレース一覧取得ボタン ---
if st.button("🔄 今日のレース一覧を取得"):
    races = get_today_race_list()
    st.session_state["races"] = races
    st.success(f"{len(races)} 件のレースを取得しました！")

# --- レースごとの表示 ---
if "races" in st.session_state:
    for race in st.session_state["races"]:
        st.subheader(race["name"])

        # 予想オッズ取得（キャッシュ）
        if f"pred_{race['url']}" not in st.session_state:
            st.session_state[f"pred_{race['url']}"] = get_predicted_odds(race["url"])

        pred_df = st.session_state[f"pred_{race['url']}"]
        st.dataframe(pred_df, use_container_width=True)

        # --- 実オッズ取得ボタン ---
        if st.button(f"🎯 {race['name']} の実オッズ取得", key=race["url"]):
            # 実オッズ取得してマージ
            actual_df = get_actual_odds(race["url"])
            merged = pd.merge(pred_df, actual_df, on="馬名", how="inner")
            merged["期待値"] = merged["実オッズ"] * merged["勝率(予想)"]
            merged = merged.sort_values("期待値", ascending=False)

            # --- 現在時刻を記録 ---
            now = datetime.datetime.now().strftime("%H:%M:%S")
            merged["時刻"] = now

            # --- 履歴保存（複数回押したら蓄積） ---
            history_key = f"history_{race['url']}"
            if history_key not in st.session_state:
                st.session_state[history_key] = merged.copy()
            else:
                st.session_state[history_key] = pd.concat(
                    [st.session_state[history_key], merged],
                    ignore_index=True
                )

            # --- グラフを描画 ---
            st.write("📈 期待値の時間推移グラフ（赤線=期待値1.0）")
            history_df = st.session_state[history_key]

            plt.figure(figsize=(10, 5))
            for name, group in history_df.groupby("馬名"):
                plt.plot(group["時刻"], group["期待値"], marker="o", label=name)
            plt.axhline(y=1.0, color="red", linestyle="--", label="期待値=1.0")
            plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
            plt.xticks(rotation=45)
            plt.ylabel("期待値")
            plt.xlabel("時刻")
            plt.tight_layout()
            st.pyplot(plt)

            # --- 表を赤ハイライトで表示 ---
            def highlight_row(row):
                if row["期待値"] >= 1.0:
                    return [f"color: red; font-weight: bold;" for _ in row]
                return ["" for _ in row]

            st.write("📊 実オッズ比較結果（期待値1.0以上 = 赤）")
            st.dataframe(merged.style.apply(highlight_row, axis=1), use_container_width=True)