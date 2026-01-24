import pandas as pd
import matplotlib.pyplot as plt
import os

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

# -----------------------------------------------
# 3. 勤務地別カウント
# -----------------------------------------------

location_counts = df["勤務地"].str.strip().value_counts()
df["都道府県"] = df["勤務地"].str.strip().str.split().str[0]
pref_counts = df["都道府県"].value_counts()

print(location_counts)
print(pref_counts)

plt.rcParams["font.family"] = "MS Gothic"

FIG_DIR = r"C:\Users\user\my_project\python\figure"
os.makedirs(FIG_DIR, exist_ok=True)

pref_counts.plot(kind="bar", figsize=(8, 5))
plt.title("都道府県別 求人数")
plt.xlabel("都道府県")
plt.ylabel("件数")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "prefecture_counts.png"))
plt.show()
