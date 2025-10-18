# utils.py
from typing import Optional

def odds_to_probability(odds: float) -> Optional[float]:
    """
    オッズ -> 勝率（1 ÷ オッズ）
    整数や文字列が入っても安全に扱い、無効な値は None を返す。
    """
    try:
        o = float(odds)
        if o <= 0:
            return None
        return round(1.0 / o, 6)  # 精度は必要なら調整
    except Exception:
        return None

def calculate_expectation(probability: float, actual_odds: float) -> Optional[float]:
    """
    期待値 = 勝率 × 実オッズ
    無効な入力があれば None を返す。
    """
    try:
        p = float(probability)
        a = float(actual_odds)
        # 負値や None を排除
        if p is None or a is None:
            return None
        return round(p * a, 6)
    except Exception:
        return None

# 小さなヘルパー（テスト用）
if __name__ == "__main__":
    # 簡単な手動テスト
    test_odds = [2.5, "3.0", 0, -1, "abc"]
    for o in test_odds:
        prob = odds_to_probability(o)
        print(f"odds={o!r} -> prob={prob}")
    print("期待値例:", calculate_expectation(odds_to_probability(2.5), 3.0))