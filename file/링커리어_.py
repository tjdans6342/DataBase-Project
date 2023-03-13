# 링커리어

from pickletools import read_unicodestring8
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from collections import defaultdict
info = defaultdict(list)

import time
import datetime

def convert_to_deadline(dday):
    if dday == '오늘마감': dday = 0
    else: dday = int(dday[2:])

    date = str(datetime.date.today()  + datetime.timedelta(days=dday))
    return date[:4] + '.' + date[5:7] + '.' + date[8:]


# Primary Setting
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(5)
driver.maximize_window()


# data crawling
url = 'https://linkareer.com/list/activity?filterBy_interestIDs=13&filterType=INTEREST&orderBy_direction=ASC&orderBy_field=RECRUIT_CLOSE_AT&page=1'
driver.get(url)
time.sleep(1)

page_num = len(driver.find_elements(By.CSS_SELECTOR, 'div.MuiBox-root > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-disableElevation')) - 3

for page in range(page_num):
    page += 2
    element = driver.find_elements(By.CSS_SELECTOR, 'div.MuiBox-root > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-disableElevation')[page]
    element.click()
    time.sleep(1)

    for i in range(3):
        driver.execute_script('scrollBy(0, 1000)')
        time.sleep(0.3)

    elements = driver.find_elements(By.CSS_SELECTOR, '.MuiBox-root > div > div.MuiBox-root > div.MuiGrid-root.MuiGrid-container > div > div')


    for element in elements:
        info['title'].append(element.find_element(By.CSS_SELECTOR, 'h5').text)
        info['deadline'].append(convert_to_deadline(element.find_element(By.CSS_SELECTOR, 'h4').text))
        info['img_url'].append(element.find_element(By.CSS_SELECTOR, '.MuiBox-root > a > div > img').get_attribute('src'))
        info['site_url'].append(element.find_element(By.CSS_SELECTOR, '.MuiBox-root > a').get_attribute('href'))

driver.close()


# save to database
data_num = len(info['title'])

data = []
for i in range(data_num):
    tmp = (info['title'][i], info['deadline'][i], info['img_url'][i], info['site_url'][i])
    data.append(tmp)

data = tuple(data)

import sqlite3
conn = sqlite3.connect(r"C:\Users\Gliver\OneDrive - jbnu.ac.kr\성문\전북대\3 - 2학기\5. 데이터베이스 [3분반]\# 프로젝트\test.db")

with conn:
	cur = conn.cursor()
	sql = 'insert into Activities(title, deadline, img_url, site_url) values(?, ?, ?, ?)'
	cur.executemany(sql, data)

print('Good')


