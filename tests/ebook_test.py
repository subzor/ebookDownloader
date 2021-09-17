
# from ebookDownloader.backend.ebook import Ebook
import pytest
import os
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from get_url import get_ebook_name



@pytest.fixture
def get_driver():
    direct_path = os.path.dirname(os.path.dirname(__file__))
    executable_path = os.path.join(direct_path, "chrome", "chromedriver.exe")
    options = Options()
    #Hide Browser
    # self.options.add_argument("--headless")
    # self.options.add_argument("--width=1300")
    # self.options.add_argument("--height=1000")
    driver = webdriver.Chrome(options=options,
                                    executable_path =executable_path)
    return driver    

# def test_title(get_driver):

#     url = "https://www.salesmanago.com/"

#     driver = get_driver
#     driver.get(url)
#     assert "SALESmanago" in driver.title


# def test_shoud_pass_when_move_toEbooksListPage(get_driver):

#     url = "https://www.salesmanago.com/"

#     driver = get_driver

#     driver.get(url)

#     try:
#         driver.wait.until(EC.presence_of_all_elements_located((By.ID, "nav-toggler")))
#     except Exception as error:
#         print("First wait ",error)
        
#     driver.find_element_by_id("nav-toggler").click()
#     time.sleep(1)

#     driver.find_elements_by_xpath('//a[contains(text(),"resources")]')[0].click()
#     time.sleep(1)

#     driver.find_elements_by_xpath('//a[contains(text(),"Ebooks")]')[0].click()
#     time.sleep(1)

#     assert "Knowledge Center" in driver.title



@pytest.mark.find_url_to_ebook
@pytest.mark.parametrize("ebook_name", [("Online Consumer Trends 2020")])
def test_shoud_pass_when_move_toSpecificEbookPage(get_driver, ebook_name):

    url = "https://www.salesmanago.com/"

    driver = get_driver

    driver.get(url)

    try:
        driver.wait.until(EC.presence_of_all_elements_located((By.ID, "nav-toggler")))
    except Exception as error:
        print("First wait ",error)
        
    driver.find_element_by_id("nav-toggler").click()
    time.sleep(1)

    driver.find_elements_by_xpath('//a[contains(text(),"resources")]')[0].click()
    time.sleep(1)

    driver.find_elements_by_xpath('//a[contains(text(),"Ebooks")]')[0].click()
    time.sleep(1)


    ebooks_list = driver.find_elements_by_xpath('//*[@class="ebook__img--container"]//a')

    list_of_links = []
    if ebooks_list:
        for ebook in ebooks_list:
            list_of_links.append(ebook.get_attribute('href'))

    time.sleep(1)


    que = Queue()

    thread_list = []
    for url in list_of_links:

        worker = Thread(target=lambda q, arg1: q.put(get_ebook_name(arg1)), args=(que, url, ebook_name))
        thread_list.append(worker)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    result = que.get()
    print(result)


    try:
        driver.get(result)
    except Exception as error:
        print(error)


    assert ebook_name in driver.title