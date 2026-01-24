import pandas as pd

# -----------------------------------------------
# 1. pandasでcsv読み込み確認
# -----------------------------------------------
df = pd.read_csv("C:/Users/user/my_project/python/korea_job_scraper/jobs.csv", encoding="utf-8")

# -----------------------------------------------
# 2. 韓国に関する求人分析
# -----------------------------------------------
korea_count = df["タグ"].str.contains("韓国語").sum()
print(f"韓国語が含まれる求人数: {korea_count}")

korea_jobs = df[df["タグ"].str.contains("韓国語")]
print(korea_jobs)

total_jobs = len(df)
korea_ratio = korea_count / total_jobs * 100
print(f"韓国語求人の割合: {korea_ratio:.2f}%")


# -----------------------------------------------
# 3. 各タグの出現回数カウント
# -----------------------------------------------
df["タグリスト"] = df["タグ"].str.split(",")

tags_series = df["タグリスト"].explode()
tags_series = tags_series.str.strip()

tag_counts = tags_series.value_counts()

print(tag_counts)
print(tag_counts.head(10))
