
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




@pytest.mark.valid_title
@pytest.mark.parametrize("url", [("https://www.salesmanago.com/")])
def test_title(url):

    direct_path = os.path.dirname(os.path.dirname(__file__))
    executable_path = os.path.join(direct_path, "chrome", "chromedriver.exe")
    options = Options()
    #Hide Browser
    # self.options.add_argument("--headless")
    # self.options.add_argument("--width=1300")
    # self.options.add_argument("--height=1000")
    driver = webdriver.Chrome(options=options,
                                    executable_path =executable_path)
    

    driver.get(url)
    assert "SALESmanago" in driver.title


@pytest.mark.go_to_ebook_page
@pytest.mark.parametrize("url", [("https://www.salesmanago.com/")])
def test_shoud_pass_when_move_toEbooksListPage(url):

    direct_path = os.path.dirname(os.path.dirname(__file__))
    executable_path = os.path.join(direct_path, "chrome", "chromedriver.exe")
    options = Options()
    #Hide Browser
    # self.options.add_argument("--headless")
    # self.options.add_argument("--width=1300")
    # self.options.add_argument("--height=1000")
    driver = webdriver.Chrome(options=options,
                                    executable_path =executable_path)
    

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

    assert "Knowledge Center" in driver.title



@pytest.mark.find_url_to_ebook
@pytest.mark.parametrize("url, ebook_name", [("https://www.salesmanago.com/"), ("Online Consumer Trends 2020")])
def test_shoud_pass_when_move_toSpecificEbookPage(url, ebook_name):

    direct_path = os.path.dirname(os.path.dirname(__file__))
    executable_path = os.path.join(direct_path, "chrome", "chromedriver.exe")
    options = Options()
    #Hide Browser
    # self.options.add_argument("--headless")
    # self.options.add_argument("--width=1300")
    # self.options.add_argument("--height=1000")
    driver = webdriver.Chrome(options=options,
                                    executable_path =executable_path)
    

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

    que = Queue()

    thread_list = []
    for url in list_of_links:

        worker = Thread(target=lambda q, arg1: q.put(get_ebook_name(arg1)), args=(que, url))
        thread_list.append(worker)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()


    try:
        driver.get(result)
    except Exception as error:
        print(error)


    assert ebook_name in driver.title