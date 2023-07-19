import time

import selenium
from selenium import webdriver
from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import csv

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
    data = pd.DataFrame()
    bodys = ['//*[@id="content"]/article/section[1]', '//*[@id="newsct_article"]']
    infogroups = driver.find_elements(By.CSS_SELECTOR, 'div.info_group')

    for i in infogroups:
        childs = i.find_elements(By.XPATH, '*')

        current_press = childs[0].text

        if len(childs) < 3:
            continue
        else:
            if childs[-1].text == '네이버뉴스':
                childs[-1].click()
                driver.switch_to.window(driver.window_handles[1])
                current_url = driver.current_url
                current_title = driver.title
                # try:
                #     current_date = driver.find_element(By.XPATH, '/html/body/div[4]/article/div[1]/header/p').text
                # except:
                #     current_date = driver.find_element(By.XPATH, '#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span').text
                
                for j in bodys:
                    try:
                        current_contents = driver.find_element(By.XPATH, j).text
                    except:
                        continue
                
                current_contents = str(current_contents).replace('\n', ' ')
                d = pd.Series([current_url, current_press, current_title, current_contents])
                data = data.append(d, ignore_index=True)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    return data

def nextpage(driver):
    button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/a[2]')
    button.click()



if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)

    df = pd.DataFrame([])

    search = '인구소멸'
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search}'
    find_pages = 10

    driver.get(url)

    for i in range(find_pages):
        singlepage = crawl_single_pages(driver=driver)
        df = df.append(singlepage, ignore_index = True)
        nextpage(driver=driver)

    print(df)
    df.to_excel(f'./crawl_{search}.xlsx', encoding='utf-8', ignore_index = True)
