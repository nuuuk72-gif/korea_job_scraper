from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# -----------------------------------------------
# 1. Chrome を起動（ヘッドレス可）
# -----------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # ブラウザ非表示
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)


# -----------------------------------------------
# 2. ローカル HTML にアクセス
# -----------------------------------------------
url = "http://localhost:8080/mock_jobs.html"
driver.get(url)

# -----------------------------------------------
# 3. 求人カード取得（CSSセレクタはHTMLに合わせる）
# -----------------------------------------------
try:
    job_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card"))
    )
except:
    job_cards = []

print(f"求人カード数: {len(job_cards)}")  # ←ここで件数確認

# -----------------------------------------------
# 4. 求人情報取得
# -----------------------------------------------
results = []
for job in job_cards:
    try:
        title = job.find_element(By.CSS_SELECTOR, ".job-title").text
    except:
        title = ""
    try:
        company = job.find_element(By.CSS_SELECTOR, ".company-name").text
    except:
        company = ""
    try:
        location = job.find_element(By.CSS_SELECTOR, ".job-location").text
    except:
        location = ""
    try:
        link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except:
        link = ""
    
    results.append([title, company, location, link])

# -----------------------------------------------
# 5. CSV に保存
# -----------------------------------------------
with open("C:/Users/user/my_project/python/korea_job_scraper/jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["タイトル", "企業名", "勤務地", "URL"])
    writer.writerows(results)

print("🎉 Selenium でのスクレイピング完了！ jobs.csv を確認してね！")

# -----------------------------------------------
# 6. ブラウザを閉じる
# -----------------------------------------------
driver.quit()
