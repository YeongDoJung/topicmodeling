import time

import selenium
from selenium import webdriver
from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import csv
import datetime

import warnings
from tqdm import tqdm
'''
&query= 검색어
&sm=tab_opt
&sort=2 0=관련도 1=최신순 2=오래된순
&photo=0
&field=0
&pd=5
&ds=2022.07.14
&de=2023.07.14
&docid=
&related=0
&mynews=0
&office_type=0
&office_section_code=0
&news_office_checked=
&nso=so%3Ar%2Cp%3A1y
&is_sug_officeid=0
'''

def crawl_single_pages(driver):
    data = pd.DataFrame([], columns=['url','신문사','작성일자','제목','내용'])
    bodys = ['//*[@id="content"]/article/section[1]', '//*[@id="newsct_article"]', '//*[@id="articeBody"]/text()']
    infogroups = driver.find_elements(By.CSS_SELECTOR, 'div.info_group')

    for i in infogroups:
        childs = i.find_elements(By.XPATH, '*')

        press = childs[0].text

        if len(childs) < 3:
            continue
        else:
            if childs[-1].text == '네이버뉴스':
                childs[-1].click()
                driver.switch_to.window(driver.window_handles[1])
                d = {'url':['NaN'],'신문사':['NaN'],'작성일자':['NaN'],'제목':['NaN'],'내용':['NaN']}
                d['url'] = [driver.current_url]
                d['제목'] = [driver.title]
                d['신문사'] = [press]
                current_date = ['NaN']

                dates = ['//*[@id="ct"]/div[1]/div[3]/div[1]/div/span', '//*[@id="ct"]/div[1]/div[3]/div[1]/div[2]/span', '//*[@id="content"]/div[1]/div/div[2]/span/em']

                for j in dates:
                    try:
                        current_date.append(driver.find_element(By.XPATH, j).text)
                    except:
                        continue
            
                d['작성일자'] = [current_date[-1]]
                
                for j in bodys:
                    try:
                        current_contents = driver.find_element(By.XPATH, j).text
                        d['내용'] = [str(current_contents).replace('\n', ' ')]

                    except:
                        continue
                
                d = pd.DataFrame(data=d)
                data = data.append(d)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    return data

def nextpage(driver):
    button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/a[2]')
    button.click()


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # options.add_argument('headless')

    driver = webdriver.Chrome()
    driver.implicitly_wait(1)

    df = pd.DataFrame([], columns=['url','신문사','작성일자','제목','내용'])

    search = '인구소멸'
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search}'
    find_pages = 100

    driver.get(url)

    for i in tqdm(range((find_pages))):
        singlepage = crawl_single_pages(driver=driver)
        df = df.append(singlepage)
        nextpage(driver=driver)

    print(df)
    now = datetime.datetime.now()
    t = now.strftime('%Y-%m-%d')
    filename = f'./data/crawl_{search}_{t}.xlsx'
    df.to_excel(filename, encoding='utf-8')
