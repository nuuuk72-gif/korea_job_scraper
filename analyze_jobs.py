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
target_cols = ["タグ", "タイトル", "説明"]

korea_count = sum(
                df[col].str.contains("韓国", na=False).sum()
                for col in target_cols
                )   

print(f"韓国に関する求人数: {korea_count}")

korea_jobs = df[df["タグ"].str.contains("韓国")]
print(korea_jobs)

total_jobs = len(df)
korea_ratio = korea_count / total_jobs * 100
print(f"韓国に関する求人の割合: {korea_ratio:.2f}%")


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


# -----------------------------------------------
# 3. 都道府県×韓国求人の分布
# -----------------------------------------------
pref_total = df["都道府県"].value_counts().sort_index()
df["韓国求人"] = df[target_cols].apply(
                    lambda row: row.str.contains("韓国", na=False).any(),
                    axis=1
                    )
pref_korea = (
            df[df["韓国求人"]]
            .groupby("都道府県")
            .size()
            .reindex(pref_total.index, fill_value=0)
            )

plt.rcParams["font.family"] = "MS Gothic"

fig, ax1 = plt.subplots(figsize=(10, 6))

# 棒グラフ（全体）
pref_total.plot(kind="bar", ax=ax1, color="skyblue")
for i, v in enumerate(pref_total):
    ax1.text(i, v, str(v), ha="center", va="bottom", fontsize=9)
ax1.set_ylabel("総求人数")
ax1.set_xlabel("都道府県")

# 線グラフ（韓国求人）
ax2 = ax1.twinx()
pref_korea.plot(kind="line", ax=ax2, marker="o", color="#EC008C")
for i, v in enumerate(pref_korea):
    ax2.text(i+0.07, v, str(v), ha="center", va="bottom", fontsize=9, color="#EC008C")
ax2.set_ylabel("韓国関連求人数")

y_max = max(pref_total.max(), pref_korea.max()) + 2.5
ax1.set_ylim(0, y_max)
ax2.set_ylim(0, y_max)

plt.title("都道府県別 求人数（韓国求人分布）")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "prefecture_korea_overlay.png"))

# -----------------------------------------------
# 4. 語学別求人数比較
# -----------------------------------------------
languages = ["韓国語", "英語", "中国語"]

language_counts = {}

for lang in languages:
    count = (
        df[target_cols]
        .apply(lambda row: row.str.contains(lang, na=False).any(), axis=1)
        .sum()
    )
    language_counts[lang] = count

lang_df = pd.DataFrame.from_dict(
    language_counts, orient="index", columns=["求人数"]
)

print(lang_df)

plt.rcParams["font.family"] = "MS Gothic"

lang_df.plot(kind="bar", legend=False, figsize=(6, 4))
plt.title("語学別 求人数比較")
plt.xlabel("語学")
plt.ylabel("求人数")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "language_counts.png"))