import requests
from selenium import webdriver
import time


def product_info_layer1(pagenumber):
    chromedriver_loc = '/Users/yinong/Downloads/chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver_loc)

    #driver.get('https://www.sephora.com/shop/lipstick?pageSize=60')
    url = 'https://www.sephora.com/shop/lipstick'
    driver.get(url+'?currentPage='+ pagenumber)
    time.sleep(5)
    button = driver.find_elements_by_xpath('//div[@class="css-111ybjq "]/button')[0]
    button.click()
    driver.execute_script("window.scrollTo(0,1500)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,2000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,2500)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,3000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,3500)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,4000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,4500)")
    time.sleep(3)
    c=0
    for a in driver.find_elements_by_xpath("//div[@class='css-12egk0t']/a"):

        print(a.get_attribute('href'))
        print(c)
        c +=1

    product_urls = [a.get_attribute('href') for a in driver.find_elements_by_xpath("//div[@class='css-12egk0t']/a")]
    brand_names = [a.text for a in driver.find_elements_by_xpath('//span[@class="css-ktoumz OneLinkNoTx"]')]
    product_names = [a.text for a in driver.find_elements_by_xpath('//span[@data-at="sku_item_name"]')]
    ratings = [a.get_attribute('aria-label') for a in driver.find_elements_by_xpath('//div[@class="css-1adflzz"]')]

    product_ids = []
    for product_urls_idv in product_urls:
        for idx in range(len(product_urls_idv)):
            if product_urls_idv[idx]=='-' and product_urls_idv[idx+1].isupper():
                start = idx+1
            if product_urls_idv[idx] == '?':
                end = idx
        product_ids.append(product_urls_idv[start:end])

    links2 = [link for link in product_urls]
    driver.close()
    return links2,brand_names,product_names,product_ids,ratings
