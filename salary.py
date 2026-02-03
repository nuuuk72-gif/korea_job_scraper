from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# -----------------------------------------------
# 1. Chrome を起動（ヘッドレス可）
# -----------------------------------------------
options = webdriver.ChromeOptions() #options : ChromeOptions のオブジェクト
options.add_argument("--headless")  # ブラウザ非表示 "--headless":Chrome に渡す実際の引数（フラグ）
options.add_argument("--no-sandbox") #.add_argument(): そのオブジェクトに引数を足すメソッド
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
        #指定したセレクタに一致する要素が ページのどこかに存在する状態になるまで待つ
    ) #.job-card の要素が出てくるまで、最大10秒待つ
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
        salary = job.find_element(By.CSS_SELECTOR, ".salary").text
    except:
        salary = ""
    try:
        description = job.find_element(By.CSS_SELECTOR, ".company-description").text
    except:
        description = ""
    try:
        tags = [tag.text for tag in job.find_elements(By.CSS_SELECTOR, ".tags .tag")]
    except:
        tags = []
    
    results.append([title, company, salary, description, tags])

    # -----------------------------------------------
# 5. CSV に保存
# -----------------------------------------------
with open("C:/Users/user/my_project/python/korea_job_scraper/salary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["タイトル", "企業名", "給与","説明", "タグ"])
    writer.writerows(results)

print("❥スクレイピング完了❥salary.csv を確認してね❥")

# -----------------------------------------------
# 6. ブラウザを閉じる
# -----------------------------------------------
driver.quit()