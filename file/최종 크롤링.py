from pickletools import read_unicodestring8
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Primary Setting
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service(executable_path=ChromeDriverManager().install())

info = []

import time
import datetime

def convert_to_deadline(dday):
    if dday == '오늘마감': dday = 0
    else: dday = int(dday[2:])

    date = str(datetime.date.today()  + datetime.timedelta(days=dday))
    return date[:4] + '.' + date[5:7] + '.' + date[8:]


# 링커리어
driver1 = webdriver.Chrome(service=service, options=chrome_options)
driver1.implicitly_wait(5)
driver1.maximize_window()

url = 'https://linkareer.com/list/activity?filterBy_interestIDs=13&filterType=INTEREST&orderBy_direction=ASC&orderBy_field=RECRUIT_CLOSE_AT&page=1'
driver1.get(url)
time.sleep(1)

page_num = len(driver1.find_elements(By.CSS_SELECTOR, 'div.MuiBox-root > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-disableElevation')) - 3

for page in range(page_num):
    page += 2
    element = driver1.find_elements(By.CSS_SELECTOR, 'div.MuiBox-root > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-disableElevation')[page]
    element.click()
    time.sleep(1)

    for i in range(3):
        driver1.execute_script('scrollBy(0, 1000)')
        time.sleep(0.3)

    elements = driver1.find_elements(By.CSS_SELECTOR, '.MuiBox-root > div > div.MuiBox-root > div.MuiGrid-root.MuiGrid-container > div > div')

    for element in elements:
        tmp = []
        tmp.append(element.find_element(By.CSS_SELECTOR, 'h5').text) # title
        tmp.append(convert_to_deadline(element.find_element(By.CSS_SELECTOR, 'h4').text)) # deadline
        tmp.append(element.find_element(By.CSS_SELECTOR, '.MuiBox-root > a > div > img').get_attribute('src')) # img_url
        tmp.append(element.find_element(By.CSS_SELECTOR, '.MuiBox-root > a').get_attribute('href')) #site_url
        info.append(tmp + [0])

driver1.close()
print(len(info))


# 캠퍼스픽
driver2 = webdriver.Chrome(service=service, options=chrome_options)
driver2.implicitly_wait(5)
driver2.maximize_window()

url = 'https://www.campuspick.com/contest?category=108'
driver2.get(url)
time.sleep(1)

for i in range(5):
    driver2.execute_script('scrollBy(0, 1000)')
    time.sleep(0.3)

elements = driver2.find_elements(By.CSS_SELECTOR, 'div.list > .item')
for element in elements:
    if element.find_element(By.CSS_SELECTOR, '.top > .info > .dday').text == '마감':
        break

    tmp = []
    tmp.append(element.find_element(By.CSS_SELECTOR, '.top > h2').text)
    tmp.append(convert_to_deadline(element.find_element(By.CSS_SELECTOR, '.top > .info > .dday').text))
    tmp.append(element.find_element(By.CSS_SELECTOR, '.top > figure').get_attribute('data-image'))
    tmp.append(element.find_element(By.CSS_SELECTOR, '.bottom> a:nth-child(1)').get_attribute('href'))
    
    is_exist = False
    for i in info:
        if tmp[0] == i[0]:
            is_exist = True
            break

    if not is_exist: 
        info.append(tmp + [0])
        

driver2.close()
print(len(info))


# 온오프믹스
def get_deadline(site_url):
    tmp_driver = webdriver.Chrome(service=service, options=chrome_options)
    tmp_driver.implicitly_wait(5)
    tmp_driver.maximize_window()

    tmp_driver.get(site_url)
    try:
        text = tmp_driver.find_element(By.CSS_SELECTOR, '.available > .letter_spc_0:nth-child(1)').text
    except:
        text = tmp_driver.find_element(By.CSS_SELECTOR, '.etc_group.date').text.split()[0]
    tmp_driver.close()

    words = text.split('.')
    text = words[0] + '.' + ('0'+words[1]+'.' if len(words[1]) == 1 else words[1]+'.') + ('0'+words[2] if len(words[2]) == 1 else words[2])

    return text

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
        
        tmp = []
        tmp.append(element.find_element(By.CSS_SELECTOR, '.title').text)
        tmp.append(element.find_element(By.CSS_SELECTOR, '.day').text)
        tmp.append(element.find_element(By.CSS_SELECTOR, '.event_thumbnail > img').get_attribute('src'))
        tmp.append(element.find_element(By.CSS_SELECTOR, '.event_area > a').get_attribute('href'))

        tmp[1] = get_deadline(tmp[3])

        is_exist = False
        for i in info:
            if tmp[0] == i[0]:
                is_exist = True
                break

        if not is_exist: 
            info.append(tmp + [0])

driver3.close()
print(len(info))


# sql과 관련된 코드 영역
import sqlite3
conn = sqlite3.connect(r'C:\Users\JSM\OneDrive - jbnu.ac.kr\성문\전북대\3 - 2학기\5. 데이터베이스 [3분반]\# 프로젝트\test.db')

with conn:
    cur = conn.cursor()

    # change detection
    bef_info = []
    cur.execute("SELECT * FROM Activities")
    table = cur.fetchall()
    for row in table:
        bef_info.append(list(row))
    
    for i in range(len(info)):
        is_new = True
        for j in range(len(bef_info)):
            if info[i][0] == bef_info[j][0]:
                is_new = False
                break

        if is_new: info[i][4] = 1

    # sort by time
    from functools import cmp_to_key

    def comp(left, right):
        l = list(map(int, left[1].split('.')))
        r = list(map(int, right[1].split('.')))

        if l[0] > r[0]: return 1
        elif l[0] < r[0]: return -1
        else: 
            if l[1] > r[1]: return 1
            elif l[1] < r[1]: return -1
            else :
                if l[2] > r[2]: return 1
                elif l[2] < r[2]: return -1
                return 0

    info = sorted(info, key=cmp_to_key(comp))
    
    # update Activites Table
    data = []
    for i in range(len(info)):
        tmp = (info[i][0], info[i][1], info[i][2], info[i][3], info[i][4])
        data.append(tmp)

    data = tuple(data)

    cur.execute('DROP TABLE IF EXISTS Activities;')
    cur.execute(r'CREATE TABLE "Activities" ("title"    TEXT, "deadline"   TEXT, "img_url"   TEXT, "site_url"  TEXT, "is_new"   INTEGER, PRIMARY KEY("title"));')

    sql = 'insert into Activities(title, deadline, img_url, site_url, is_new) values(?, ?, ?, ?, ?);'
    cur.executemany(sql, data)

print('Good')