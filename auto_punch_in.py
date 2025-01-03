import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import argparse

root_path = 'C:/Users/Hua/Desktop/auto-punch-in/'
log_file_name = 'log.txt'

# google chrome driver (如果 chrome 更新可能會失效)
driver_name = r'chromedriver-win64_v131/chromedriver.exe'
driver_path = root_path + driver_name

# 識別證號碼
id = 'Hua'
password = 'Testing'

# 打卡網址
target_url = 'https://eadm.ncku.edu.tw/welldoc/ncku/iftwd/signIn.php'

# 放假或請假的檔案路徑(這時不應該打卡)
skip_date_path = root_path + 'skip_dates.txt'

# 設定日誌檔案與格式
logging.basicConfig(
    filename= root_path + log_file_name,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

parser = argparse.ArgumentParser(description="處理模式參數")
parser.add_argument('--mode', type=str, required=True, help="執行模式，例如 punch_in 或 check_out")
args = parser.parse_args()

logging.info("------------auto punch-in start------------")

# skip day check
def skip_execution():
    try:
        if not os.path.exists(skip_date_path):
            logging.info("skip_dates file not exist: %s", skip_date_path)
            return False

        with open(skip_date_path, 'r') as f:
            skip_dates = [line.strip() for line in f if line.strip()]

        today = datetime.now().strftime('%Y-%m-%d')

        if today in skip_dates:
            logging.info("Today is a skip day")
            return True
        else:
            logging.info("Today is not a skip day")
            return False
    except Exception as e:
        logging.error("skip day check fatal error: %s", str(e))
        return False


if skip_execution():
    logging.info("end mission")
else:
    try:
        # 建立 Service 物件來指定 WebDriver 的路徑
        service = Service(driver_path)

        # 建立 ChromeOptions 物件
        chrome_options = webdriver.ChromeOptions()

        # 使用指定的 WebDriver 路徑來初始化 WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(target_url)

        # 等待網站載入
        time.sleep(2)

        # 帳號欄位
        account_box = driver.find_element(By.ID, 'psnCode')
        account_box.send_keys(id)
        logging.info("enter account: %s", id)

        # 密碼欄位
        code_box = driver.find_element(By.ID, 'password')
        code_box.send_keys(password)
        logging.info("enter passward: %s", password)

        # 簽到 or 簽退按鈕
        if args.mode == "punch_in":
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-success.pull-left')
            logging.info("punch in submit")
        elif args.mode == "check_out":
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-warning.pull-left')
            logging.info("check out submit")
            
        submit_button.click()

        # 等待操作完成
        time.sleep(3)

    except Exception as e:
        logging.error("Fatal error: %s", str(e))

    finally:
        # 關閉瀏覽器
        driver.quit()
        logging.info("end mission")
