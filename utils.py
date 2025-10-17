%%bash
cat > utils.py <<'PY'
# ここに上の utils.py のコードを丸ごと貼る
PY
python - <<'PY'
import utils
print("utils loaded OK")
print("2.5 ->", utils.odds_to_probability(2.5))
print("期待値:", utils.calculate_expectation(utils.odds_to_probability(2.5), 3.0))
PY