
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


# def test_shoud_pass_when_get_list_of_urls(get_driver):

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


#     ebooks_list = driver.find_elements_by_xpath('//*[@class="ebook__img--container"]//a')

#     list_of_links = []
#     if ebooks_list:
#         for ebook in ebooks_list:
#             list_of_links.append(ebook.get_attribute('href'))

#     assert isinstance(list_of_links, list)


# @pytest.mark.find_url_to_ebook
# @pytest.mark.parametrize("ebook_name", [("Online Consumer Trends 2020")])
# def test_shoud_pass_when_move_toSpecificEbookPage(get_driver, ebook_name):

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


#     ebooks_list = driver.find_elements_by_xpath('//*[@class="ebook__img--container"]//a')

#     list_of_links = []
#     if ebooks_list:
#         for ebook in ebooks_list:
#             list_of_links.append(ebook.get_attribute('href'))

#     time.sleep(1)

#     que = Queue()

#     thread_list = []

#     for url in list_of_links:

#         worker = Thread(target=get_ebook_name, args=(que, url, ebook_name))
#         thread_list.append(worker)
#     for thread in thread_list:
#         thread.start()
#     for thread in thread_list:
#         thread.join()

#     correct_url = que.get()

#     try:
#         driver.get(correct_url)
#     except Exception as error:
#         print(error)


#     assert ebook_name in driver.title


@pytest.mark.find_url_to_ebook
@pytest.mark.parametrize("ebook_name, email", [("Online Consumer Trends 2020", 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com')])
def test_shoud_pass_when_move_toSpecificEbookPage(get_driver, ebook_name, email):

    url = "https://www.salesmanago.com/"

    details = {
    "ebook_name" : ebook_name,
    "name" : "Daniel Test",
    "email" : email,
    "company" : "Recruitment task",
    "website" : "www.google.pl",
    "country" : "Poland",
    "country_code" : "+48",
    "phone" : "555666777"
}


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

        worker = Thread(target=get_ebook_name, args=(que, url, ebook_name))
        thread_list.append(worker)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    correct_url = que.get()

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)



        time.sleep(3)

    driver.find_element_by_name("name").send_keys(details['name'])
    driver.find_element_by_id("email").send_keys(details['email'])
    driver.find_element_by_name("company").send_keys(details['company'])
    driver.find_element_by_name("url").send_keys(details['website'])
    country_select = Select(driver.find_element_by_id("countryOptions"))
    country_select.select_by_visible_text(details['country'])
    driver.find_element_by_name("phoneNumber").send_keys(details['phone'])

    try:
        chat_frame = driver.find_element_by_class_name("bhr-chat__messenger")
        driver.switch_to.frame(chat_frame)
        driver.find_element_by_class_name("bhr-chat-messenger__minimalise").click()
        driver.switch_to.default_content()
    except Exception as error:
        print(error)

    driver.find_element_by_xpath('//*[@class="fa fa-angle-right fa-lg"]').click()

    time.sleep(1)


    assert "The ebook has been sent to your email address." in driver.find_element_by_xpath('//*[@class="thanks-message"]').getText()
