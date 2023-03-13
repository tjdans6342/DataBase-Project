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


# Primary Setting
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service(executable_path=ChromeDriverManager().install())



# data crawling
driver3 = webdriver.Chrome(service=service, options=chrome_options)
driver3.implicitly_wait(5)
driver3.maximize_window()

url = 'https://www.onoffmix.com/event/main/?c=092'
driver3.get(url)
time.sleep(1)

driver3.find_element(By.CSS_SELECTOR, '#content > div > section.keyword_search_area > form > fieldset.filter_category_area > span').click()
time.sleep(0.5)
driver3.find_element(By.CSS_SELECTOR, '#interest_category_01').click()
driver3.find_element(By.CSS_SELECTOR, '#interest_category_02').click()
driver3.find_element(By.CSS_SELECTOR, '#content > div > section.keyword_search_area > form > fieldset.filter_category_area.open > div > div > div > button').click()
time.sleep(0.5)

driver3.find_element(By.CSS_SELECTOR, '#content > div > section.keyword_search_area > form > fieldset.filter_time_pay_type > span').click()
time.sleep(0.5)
driver3.find_element(By.CSS_SELECTOR, '#free').click()
driver3.find_element(By.CSS_SELECTOR, '#content > div > section.keyword_search_area > form > fieldset.filter_time_pay_type.open > div > div > div > button').click()
time.sleep(0.5)

search_box = driver3.find_element(By.CSS_SELECTOR, '#keywordSearch')
search_box.send_keys('IT')
search_box.send_keys(Keys.ENTER)
time.sleep(1)

driver3.find_element(By.CSS_SELECTOR, '#content > div > section.event_main_area > div.title_bar > ul.view_mode > li.btn_list').click()
time.sleep(0.5)
driver3.find_element(By.CSS_SELECTOR, '#content > div > section.event_main_area > div.title_bar > ul.sort_menu > li:nth-child(3) > a').click()
time.sleep(1)

is_stop = False
for i in range(2, 5):
    if is_stop: 
        break

    driver3.find_element(By.CSS_SELECTOR, f'#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child({i})').click()
    time.sleep(0.5)

    elements = driver3.find_elements(By.CSS_SELECTOR, '#content > div > section.event_main_area > ul > li')
    
    for element in elements:  
        try:
            element.find_element(By.CSS_SELECTOR, '.day')
        except:
            is_stop = True
            break

        if 'cs' in element.find_element(By.CSS_SELECTOR, '.event_area > a').get_attribute('href'):
            continue
        
        info['title'].append(element.find_element(By.CSS_SELECTOR, '.title').text)
        info['deadline'].append(element.find_element(By.CSS_SELECTOR, '.day').text)
        info['img_url'].append(element.find_element(By.CSS_SELECTOR, '.event_thumbnail > img').get_attribute('src'))
        info['site_url'].append(element.find_element(By.CSS_SELECTOR, '.event_area > a').get_attribute('href'))


driver3.close()

data_num = len(info['title'])
print(f'개수: {data_num}')

for i in range(data_num):
    print(f'[{i+1}번째 대외활동]')
    print(info['title'][i])
    print(info['img_url'][i])
    print(info['site_url'][i])
    print(info['deadline'][i])
    print()


print('Good')


