import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------------------------
# 1. pandasでcsv読み込み確認
# -----------------------------------------------
df = pd.read_csv("C:/Users/user/my_project/python/korea_job_scraper/salary.csv", encoding="utf-8")

# -----------------------------------------------
# 2. スキル別給与分析
# -----------------------------------------------
import re

def extract_salary(text):
    if pd.isna(text):
        return None
    
    if "時給" in text:
        match = re.search(r"(\d+)", text)
        if match:
            hourly = int(match.group(1))
            return hourly * 8 * 20 * 12 / 10000
        
    if "年収" in text:
       # 年収 400〜600万円 のパターン
        match = re.search(r"(\d+)〜(\d+)", text)
        if match:
            low = int(match.group(1))
            high = int(match.group(2))
            return (low + high) / 2

        # 年収 500万円～ のパターン
        match = re.search(r"(\d+)", text)
        if match:
            return int(match.group(1))

        return None

df["年収数値"] = df["給与"].apply(extract_salary)

target_cols = ["タグ", "タイトル", "説明"]

skills = ["韓国", "英語", "中国語"]
salary_results = {}

for skill in skills:
    mask = df[target_cols].apply(
        lambda row: row.str.contains(skill, na=False).any(),
        axis=1
    )
    avg_salary = df[mask]["年収数値"].mean()
    salary_results[skill] = avg_salary
    print(f"{skill}求人の平均年収: {avg_salary:.1f}万円")

# -----------------------------------------------
# 3. スキル別給与グラフ表示
# -----------------------------------------------

plt.rcParams["font.family"] = "MS Gothic"

FIG_DIR = r"C:\Users\user\my_project\python\figure_salary"
os.makedirs(FIG_DIR, exist_ok=True)

salary_series = pd.Series(salary_results)

salary_series.plot(kind="bar", figsize=(8, 5))
plt.title("スキル別給与の平均")
plt.xlabel("スキル")
plt.ylabel("平均年収(万円)")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "skill_salary.png"))