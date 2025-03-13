import argparse
import logging
import os
import time
from datetime import datetime
from typing import Dict

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# 打卡網址
TARGET_URL = 'https://eadm.ncku.edu.tw/welldoc/ncku/iftwd/signIn.php'

# 日誌檔案路徑
log_file_name = os.path.join(ROOT_PATH, 'log.txt')
# 放假或請假的檔案路徑(這時不應該打卡)
skip_date_path = os.path.join(ROOT_PATH, 'skip_dates.txt')

# 設定日誌檔案與格式
logging.basicConfig(
    filename= log_file_name,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_args():
    parser = argparse.ArgumentParser(description="處理模式參數")
    parser.add_argument('--mode', type=str, required=True, help="執行模式，例如 punch_in 或 check_out")
    parser.add_argument('--dry-run', action='store_true', help="是否為測試模式")
    args = parser.parse_args()
    return args

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

def get_webdriver(service, driver_type):
    if driver_type == 'chrome':
        return webdriver.Chrome(service=service, options=webdriver.ChromeOptions())
    elif driver_type == 'firefox':
        return webdriver.Firefox(service=service, options=webdriver.FirefoxOptions())
    elif driver_type == 'edge':
        return webdriver.Edge(service=service, options=webdriver.EdgeOptions())
    else:
        raise ValueError("Invalid driver type: %s" % driver_type)

def try_punch(args: Dict) -> None:
    logging.info("------------auto punch-in start------------")
    if skip_execution():
        logging.info("end mission")
    else:
        # google chrome driver (如果 chrome 更新可能會失效)
        driver_name = os.getenv('DRIVER_NAME')
        driver_type = os.getenv('DRIVER_TYPE')
        driver_path = os.path.join(ROOT_PATH, driver_name)
        # 建立 Service 物件來指定 WebDriver 的路徑
        service = Service(driver_path)

        # 建立 ChromeOptions 物件
        driver = get_webdriver(service, driver_type)

        driver.get(TARGET_URL)
        try:

            # 等待網站載入
            time.sleep(2)

            # 帳號欄位
            account_box = driver.find_element(By.ID, 'psnCode')
            user_id = os.getenv('USER_ID')
            account_box.send_keys(user_id)
            logging.info("enter account: %s", user_id)

            # 密碼欄位
            code_box = driver.find_element(By.ID, 'password')
            password = os.getenv('USER_PASSWORD')
            code_box.send_keys(password)
            logging.info("enter passward: %s", password)


            # 簽到 or 簽退按鈕
            if args.mode == "punch_in":
                submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-success.pull-left')
                logging.info("punch in submit")
            elif args.mode == "check_out":
                submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-warning.pull-left')
                logging.info("check out submit")
                
            if not args.dry_run:
                submit_button.click()
            else:
                logging.info("dry run - click submit button")

            # 等待操作完成
            time.sleep(3)

        except Exception as e:
            logging.error("Fatal error: %s", str(e))

        finally:
            # 關閉瀏覽器
            driver.quit()
            logging.info("end mission")


if __name__ == '__main__':
    args = parse_args()
    load_dotenv()
    try_punch(args)