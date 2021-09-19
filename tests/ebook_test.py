
import pytest
import os
import time
import requests
from threading import Thread
from queue import Queue
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from get_url import get_ebook_name


def go_to_destination(driver):

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "nav-toggler")))
    except Exception as error:
        print(error)

    driver.find_element_by_id("nav-toggler").click()
    time.sleep(1)

    driver.find_elements_by_xpath('//a[contains(text(),"resources")]')[0].click()
    time.sleep(1)

    driver.find_elements_by_xpath('//a[contains(text(),"Ebooks")]')[0].click()
    time.sleep(1)

def get_ebooks_list(driver):

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="ebook__img--container"]//a')))
    except Exception as error:
        print(error)

    ebooks_list = driver.find_elements_by_xpath('//*[@class="ebook__img--container"]//a')

    list_of_links = []
    if ebooks_list:
        for ebook in ebooks_list:
            list_of_links.append(ebook.get_attribute('href'))
    return list_of_links

def get_url_from_thread(list_of_links, ebook_name):
    que = Queue()

    thread_list = []

    for url in list_of_links:
        worker = Thread(target=get_ebook_name, args=(que, url, ebook_name))
        thread_list.append(worker)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    return que.get()


def minimalise_chat_and_click_forward(driver):
    try:
        chat_frame = driver.find_element_by_class_name("bhr-chat__messenger")
        driver.switch_to.frame(chat_frame)
        driver.find_element_by_class_name("bhr-chat-messenger__minimalise").click()
        driver.switch_to.default_content()
    except Exception as error:
        print(error)

    driver.find_element_by_xpath('//*[@class="fa fa-angle-right fa-lg"]').click()

def set_input_boxes(driver, details):

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="fa fa-angle-right fa-lg"]')))
    except Exception as error:
        print(error)

    driver.find_element_by_name("name").send_keys(details['name'])
    driver.find_element_by_id("email").send_keys(details['email'])
    driver.find_element_by_name("company").send_keys(details['company'])
    driver.find_element_by_name("url").send_keys(details['website'])
    country_select = Select(driver.find_element_by_id("countryOptions"))
    country_select.select_by_visible_text(details['country'])
    driver.find_element_by_name("phoneNumber").send_keys(details['phone'])

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
    driver.implicitly_wait(1)
    return driver

@pytest.fixture
@pytest.mark.find_url_to_ebook
@pytest.mark.parametrize("ebook_name", [("Online Consumer Trends 2020")])
def get_ebook_url(get_driver, ebook_name):

    url = "https://www.salesmanago.com/"

    driver = get_driver

    driver.get(url)

    go_to_destination(driver=driver)

    list_of_links = get_ebooks_list(driver=driver)
    time.sleep(1)

    correct_url = get_url_from_thread(list_of_links=list_of_links, ebook_name=ebook_name)

    return correct_url

@pytest.mark.find_title
def test_title(get_driver):

    url = "https://www.salesmanago.com/"

    driver = get_driver
    driver.get(url)
    assert "SALESmanago" in driver.title

@pytest.mark.move_to_ebook_list
def test_shoud_pass_when_move_toEbooksListPage(get_driver):

    url = "https://www.salesmanago.com/"

    driver = get_driver

    driver.get(url)

    go_to_destination(driver=driver)

    time.sleep(1)

    assert "Knowledge Center" in driver.title

def test_shoud_pass_when_get_list_of_urls(get_driver):

    url = "https://www.salesmanago.com/"

    driver = get_driver

    driver.get(url)

    go_to_destination(driver=driver)

    list_of_links = get_ebooks_list(driver=driver)

    assert (isinstance(list_of_links, list) and (len(list_of_links) > 0 ))

@pytest.mark.find_url_to_ebook
@pytest.mark.parametrize("ebook_name", [("Online Consumer Trends 2020")])
def test_shoud_pass_when_move_toSpecificEbookPage(get_driver, get_ebook_url, ebook_name):

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    assert ebook_name in driver.title

@pytest.mark.check_name
@pytest.mark.parametrize("ebook_name, name", [("Online Consumer Trends 2020", 'Da')])
def test_shoud_pass_when_nameIsInvalid(get_driver, get_ebook_url, ebook_name, name):


    details = {
                "ebook_name" : ebook_name,
                "name" : name
                }

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    driver.find_element_by_name("name").send_keys(details['name'])

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert "Please enter at least 3 characters." in driver.find_element_by_xpath('//*[@id="name-error"]').text

@pytest.mark.check_email
@pytest.mark.parametrize("ebook_name, name, email", [("Online Consumer Trends 2020", "Daniel", 'daniel.wincencik.benhauer+test@gmail.com')])
def test_shoud_pass_when_emailIsInvalid(get_driver, get_ebook_url, ebook_name, name, email):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    driver.find_element_by_name("name").send_keys(details['name'])
    driver.find_element_by_id("email").send_keys(details['email'])

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert "Please enter your business email." in driver.find_element_by_xpath('//*[@id="email-error"]').text

@pytest.mark.check_company
@pytest.mark.parametrize("ebook_name, name, email, company", [("Online Consumer Trends 2020", "Daniel" , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', '')])
def test_shoud_pass_when_companyIsInvalid(get_driver, get_ebook_url, ebook_name, name, email, company):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    driver.find_element_by_name("name").send_keys(details['name'])
    driver.find_element_by_id("email").send_keys(details['email'])
    driver.find_element_by_name("company").send_keys(details['company'])

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert "This field is required." in driver.find_element_by_xpath('//*[@id="company-error"]').text

@pytest.mark.check_website
@pytest.mark.parametrize("ebook_name, name, email, company, website", [("Online Consumer Trends 2020", "Daniel" , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', 'TestCompany', "test")])
def test_shoud_pass_when_websiteIsInvalid(get_driver, get_ebook_url, ebook_name, name, email, company, website):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company,
                "website" : website
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    driver.find_element_by_name("name").send_keys(details['name'])
    driver.find_element_by_id("email").send_keys(details['email'])
    driver.find_element_by_name("company").send_keys(details['company'])
    driver.find_element_by_name("url").send_keys(details['website'])

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert "Please, insert correct URL" in driver.find_element_by_xpath('//*[@id="url-error"]').text

@pytest.mark.check_country
@pytest.mark.parametrize("ebook_name, name, email, company, website, country", [("Online Consumer Trends 2020", "Daniel" , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', 'TestCompany', 'test.pl' ,"Pland")])
def test_shoud_pass_when_countryIsInvalid(get_driver, get_ebook_url, ebook_name, name, email, company, website, country):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company,
                "website" : website,
                "country" : country
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    driver.find_element_by_name("name").send_keys(details['name'])
    driver.find_element_by_id("email").send_keys(details['email'])
    driver.find_element_by_name("company").send_keys(details['company'])
    driver.find_element_by_name("url").send_keys(details['website'])
    country_select = Select(driver.find_element_by_id("countryOptions"))
    try:
        country_select.select_by_visible_text(details['country'])
        assert False
    except Exception as e:
        assert True

@pytest.mark.check_phone_number_empty
@pytest.mark.parametrize("ebook_name, name, email, company, website, country, phone", [('Online Consumer Trends 2020', 'Daniel' , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', 'TestCompany', 'test.pl', 'Poland', '55666777')])
def test_shoud_pass_when_phoneIsEmpty(get_driver, get_ebook_url, ebook_name, name, email, company, website, country, phone):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company,
                "website" : website,
                "country" : country,
                "phone" : phone
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    set_input_boxes(driver=driver, details=details)

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert driver.find_element_by_id("phoneNumber-error").is_displayed()


@pytest.mark.check_phone_number
@pytest.mark.parametrize("ebook_name, name, email, company, website, country, phone", [('Online Consumer Trends 2020', 'Daniel' , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', 'Test', 'test.pl', 'Poland', '55666777')])
def test_shoud_pass_when_phoneIsInvalid(get_driver, get_ebook_url, ebook_name, name, email, company, website, country, phone):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company,
                "website" : website,
                "country" : country,
                "phone" : phone
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    set_input_boxes(driver=driver, details=details)

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert driver.find_element_by_xpath('//*[@class="error diallingCode-error"]').is_displayed()


@pytest.mark.get_direct_download_url
@pytest.mark.parametrize("ebook_name, name, email, company, website, country, phone", [('Online Consumer Trends 2020', 'Daniel' , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', 'Test', 'test.pl', 'Poland', '555666777')])
def test_shoud_pass_when_moveToThanksPage(get_driver, get_ebook_url, ebook_name, name, email, company, website, country, phone):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company,
                "website" : website,
                "country" : country,
                "phone" : phone
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)


    time.sleep(1)

    set_input_boxes(driver=driver, details=details)

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    assert driver.find_element_by_xpath('//*[@class="thanks-message"]').is_displayed()


@pytest.mark.check_file_exist
@pytest.mark.parametrize("ebook_name, name, email, company, website, country, phone", [('Online Consumer Trends 2020', 'Daniel' , 'daniel.wincencik.benhauer+testrekrutacja@salesmanago.com', 'Test', 'test.pl', 'Poland', '555666777')])
def test_shoud_pass_when_ebookExist(get_driver, get_ebook_url, ebook_name, name, email, company, website, country, phone):

    details = {
                "ebook_name" : ebook_name,
                "name" : name,
                "email" : email,
                "company" : company,
                "website" : website,
                "country" : country,
                "phone" : phone
            }

    driver = get_driver

    correct_url = get_ebook_url

    driver = get_driver

    try:
        driver.get(correct_url)
    except Exception as error:
        print(error)

    time.sleep(1)

    set_input_boxes(driver=driver, details=details)

    try:
        minimalise_chat_and_click_forward(driver=driver)
    except Exception as error:
        print(error)

    time.sleep(1)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(text(),"HERE")]')))
    except Exception as error:
        print(error)
    link_to_pdf = driver.find_element_by_xpath('//a[contains(text(),"HERE")]').get_attribute("href")

    time.sleep(1)

    r = requests.get(link_to_pdf, allow_redirects=True)

    open(os.path.join(os.path.dirname(__file__), "download", details["ebook_name"] + ".pdf"), 'wb').write(r.content)

    is_file = os.path.isfile(os.path.join(os.path.dirname(__file__),"download" ,details["ebook_name"] + ".pdf"))

    assert is_file
