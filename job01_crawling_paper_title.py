from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


# Notice
#
# crawling paper titles main category
#


# Web driver setting
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

# Webdriver setting
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = options)

# Paper category
category = ['인문학', '사회과학', '자연과학', '공학', '의학학', '농수해양', '예술체육', '복합학']

# Create a empty DataFrame
df_titles = pd.DataFrame()


# Data crawling
for i in range(len(category)):

    url = 'https://www.kci.go.kr/kciportal/po/search/poArtiSearList.kci'                # reset browser
    driver.get(url)

    category_btn_xpath = '//*[@id="conLeft"]/div/div[1]/ul/li[{}]'.format((i + 1))      # select category
    time.sleep(0.3)
    driver.find_element(By.XPATH, category_btn_xpath).click()

    select_btn = '//*[@id="conLeft"]/div/div[2]'                                        # search button
    time.sleep(0.3)
    driver.find_element(By.XPATH, select_btn).click()

    titles = []                                                 # Create empty list for save headline


    for j in range(200):                                        # Category each 10,000

        for k in range(50):
            title_xpath = '//*[@id="poArtiSearList"]/table/tbody/tr[{}]/td[3]/a'.format((k + 1))

            try:
                title = driver.find_element(By.XPATH, title_xpath).text
                title = re.compile('[^가-힣A-Za-z ]').sub('', title)        # Repalce all to 'null' execpt "가 ~ 힣, A ~ Z, a ~ z, space"
                title = (title.lower())                                         # Convert uppercase letters to lowercase
                titles.append(title)

                print(title)
            except:
                print(i, j, k)

        next_button_xpath = '//*[@id="contents"]/div[2]/div[2]/div/a[12]'
        driver.execute_script('window.scrollTo(0, 20000)')                      # scroll to the bottom of the site to activate button
        time.sleep(0.8)
        driver.find_element(By.XPATH, next_button_xpath).click()


    df_section_titles = pd.DataFrame(titles, columns = ['titles'])              # Create columns 'titles'
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows', ignore_index = True)


driver.close()                                                 # close browser

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/KCL_titles_total_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False) # Change time format to 'YYYYMMDD'
                                                                # index = False == 0, 1, 2 default index = False
