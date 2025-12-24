import pandas as pd

# -----------------------------------------------
# 1. pandasでcsv読み込み確認
# -----------------------------------------------
df = pd.read_csv("C:/Users/user/my_project/python/korea_job_scraper/jobs.csv", encoding="utf-8")
print(df.head())
print("件数:", len(df))
print(df.columns)
print(df.info())