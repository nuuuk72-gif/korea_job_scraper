import pandas as pd

# -----------------------------------------------
# 1. pandasでcsv読み込み確認
# -----------------------------------------------
df = pd.read_csv("C:/Users/user/my_project/python/korea_job_scraper/jobs.csv", encoding="utf-8")

# -----------------------------------------------
# 2. 韓国に関する求人の抽出
# -----------------------------------------------
korea_count = df["タグ"].str.contains("韓国語").sum()
print(f"韓国語が含まれる求人数: {korea_count}")

korea_jobs = df[df["タグ"].str.contains("韓国語")]
print(korea_jobs)

# -----------------------------------------------
# 3. 韓国に関する求人の割合計算
# -----------------------------------------------
total_jobs = len(df)
korea_ratio = korea_count / total_jobs * 100
print(f"韓国語求人の割合: {korea_ratio:.2f}%")

