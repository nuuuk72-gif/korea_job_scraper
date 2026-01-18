import pandas as pd

# -----------------------------------------------
# 1. pandasでcsv読み込み確認
# -----------------------------------------------
df = pd.read_csv("C:/Users/user/my_project/python/korea_job_scraper/jobs.csv", encoding="utf-8")
korea_count = df["タグ"].str.contains("韓国語").sum()
print(f"韓国語が含まれる求人数: {korea_count}")

korea_jobs = df[df["タグ"].str.contains("韓国語")]
print(korea_jobs)
