# 캠퍼스픽

from pickletools import read_unicodestring8
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from collections import defaultdict
import time
import copy

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

info = defaultdict(list)

# data crawling
url = 'https://www.campuspick.com/contest?category=108'
driver.get(url)
time.sleep(1)

for i in range(5):
    driver.execute_script('scrollBy(0, 1000)')
    time.sleep(0.3)

elements = driver.find_elements(By.CSS_SELECTOR, 'div.list > .item')
for element in elements:
    if element.find_element(By.CSS_SELECTOR, '.top > .info > .dday').text == '마감':
        break

    info['title'].append(element.find_element(By.CSS_SELECTOR, '.top > h2').text)
    info['deadline'].append(convert_to_deadline(element.find_element(By.CSS_SELECTOR, '.top > .info > .dday').text))
    info['img_url'].append(element.find_element(By.CSS_SELECTOR, '.top > figure').get_attribute('data-image'))
    info['site_url'].append(element.find_element(By.CSS_SELECTOR, '.bottom> a:nth-child(1)').get_attribute('href'))

driver.close()


# save to database
data_num = len(info['title'])
print(data_num)

# data = []
# for i in range(data_num):
#     tmp = (info['title'][i], info['deadline'][i], info['img_url'][i], info['site_url'][i])
#     data.append(tmp)

# data = tuple(data)

# import sqlite3
# conn = sqlite3.connect(r"C:\Users\Gliver\OneDrive - jbnu.ac.kr\성문\전북대\3 - 2학기\5. 데이터베이스 [3분반]\# 프로젝트\test.db")

# with conn:
# 	cur = conn.cursor()
# 	sql = 'insert into Activities(title, deadline, img_url, site_url) values(?, ?, ?, ?)'
# 	cur.executemany(sql, data)

print('Good')


