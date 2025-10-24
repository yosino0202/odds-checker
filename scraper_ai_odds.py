import asyncio
from playwright.async_api import async_playwright
import csv
import os
import subprocess

async def fetch_ai_predicted_odds(race_id="202508030911"):
    url = f"https://race.netkeiba.com/odds/index.html?race_id={race_id}"
    print(f"🔍 AI予想オッズページにアクセス中... ({url})")

    os.makedirs("data", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        html = await page.content()
        with open("data/debug_ai.html", "w", encoding="utf-8") as f:
            f.write(html)

        horses = await page.eval_on_selector_all("td.HorseInfo div.HorseName a", "els => els.map(e => e.textContent.trim())")
        odds = await page.eval_on_selector_all("td.Odds span", "els => els.map(e => e.textContent.trim())")

        await browser.close()

    print(f"🐴 horses={len(horses)}, odds={len(odds)}")

    if len(horses) == 0:
        print("⚠️ データが取得できません。構造を確認してください。")
        return

    with open("data/ai_odds.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["race_id", "horse", "predicted_odds"])
        for h, o in zip(horses, odds):
            writer.writerow([race_id, h, o])

    print(f"✅ {len(horses)} 件のAI予想オッズを data/ai_odds.csv に保存しました。")

def push_to_github():
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")

    if not repo or not token:
        print("⚠️ GitHubの認証情報が見つかりません。")
        return

    subprocess.run(["git", "init"])
    subprocess.run(["git", "config", "user.name", "replit-bot"])
    subprocess.run(["git", "config", "user.email", "replit@bot.com"])
    subprocess.run(["git", "remote", "add", "origin", f"https://{token}@github.com/{repo}.git"])
    subprocess.run(["git", "add", "data/ai_odds.csv", "data/debug_ai.html"])
    subprocess.run(["git", "commit", "-m", "Auto update AI odds"])
    subprocess.run(["git", "push", "-f", "origin", "main"])
    print("✅ GitHubに push 完了！")

if __name__ == "__main__":
    asyncio.run(fetch_ai_predicted_odds())
    push_to_github()