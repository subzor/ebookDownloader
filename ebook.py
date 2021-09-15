from typing import Dict
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from threading import Thread, excepthook
import requests
from bs4 import BeautifulSoup


class Ebook:

    def __init__(self, account: Dict):


        self.account = account
        self.salesmanago_url = "https://www.salesmanago.com/"
        self.direct_path = os.path.dirname(__file__)
        self.executable_path = os.path.join(self.direct_path, "chrome", "chromedriver.exe")
        self.options = Options()
        #Hide Browser
        # self.options.add_argument("--headless")
        # self.options.add_argument("--width=1300")
        # self.options.add_argument("--height=1000")
        self.driver = webdriver.Chrome(options=self.options,
                                        executable_path =self.executable_path)

        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1)


    def get_url(self):
        self.driver.get(self.salesmanago_url)
        

        try:
            self.wait.until(EC.presence_of_all_elements_located((By.ID, "nav-toggler")))
        except Exception as error:
            print("First wait ",error)
        
        self.driver.find_element_by_id("nav-toggler").click()

        self.resources = self.driver.find_elements_by_xpath('//a[contains(text(),"resources")]')
        time.sleep(1)
        self.resources[0].click()

        self.ebooks_btn = self.driver.find_elements_by_xpath('//a[contains(text(),"Ebooks")]')
        time.sleep(1)
        self.ebooks_btn[0].click()
        
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "article-content")))
        except Exception as error:
            print("First wait ",error)

        self.ebooks_list = self.driver.find_elements_by_xpath('//*[@class="ebook__img--container"]//a')

        self.list_of_links =[]

        for i in self.ebooks_list:
            self.list_of_links.append(i.get_attribute('href')) 


        thread_list = []
        for url in self.list_of_links:
            worker = Thread(target=self.get_ebook_name,args=(url,))
            thread_list.append(worker)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()



        self.driver.get(self.correct_url)
    
        time.sleep(3)

        # abc = self.driver.find_element_by_xpath('//label[contains(text(),"Name and surname")]') #.send_keys(self.account['name'])
        self.driver.find_element_by_name("name").send_keys(self.account['name'])
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(self.account['email'])
        # self.driver.find_element_by_xpath('//label[contains(text(),"Business email")]').send_keys(self.account['email'])

        # self.driver.find_element_by_xpath('//label[contains(text(),"Company")]').send_keys(self.account['company'])
        self.driver.find_element_by_name("company").send_keys(self.account['company'])
        self.driver.find_element_by_name("url").send_keys(self.account['website'])

        country_select = Select(self.driver.find_element_by_id("countryOptions"))
        country_select.select_by_visible_text(self.account['country'])
        # self.driver.find_element_by_xpath('//label[contains(text(),"Name and surname")]').send_keys(self.account['country'])
        # self.driver.find_element_by_name("phoneDiallingCode").send_keys(self.account['country_code'])
        self.driver.find_element_by_name("phoneNumber").send_keys(self.account['phone'])
        self.driver.find_element_by_xpath('//*[@class="fa fa-angle-right fa-lg"]').click()

        time.sleep(3)
        lol = self.driver.find_element_by_xpath('//a[contains(text(),"HERE")]').get_attribute("href")

        time.sleep(3)

        r = requests.get(lol, allow_redirects=True)

        open(self.account["ebook_name"] + ".pdf", 'wb').write(r.content)


    def get_ebook_name(self, url):

        headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
        "action": "sign-in"
        }
        try:
            requests_session = requests.Session()
            requests_session.headers = headers
            page = requests_session.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'lxml',from_encoding=page.encoding)
        except Exception as error:
            print(error)
        try:
            name = soup.find("h1",attrs={"class": "ebook__title text-center"}).getText()
        except Exception as error:
            print(error)
            name = soup.find("h1",attrs={"class": "register-form__headline register-form__headline--pro"}).getText()

        if self.account['ebook_name'] in name:
            self.correct_url = url





if __name__ == "__main__":
    

    details = {
        "ebook_name" : "Complete Marketing Automation Product Profile",
        "name" : "Daniel Test",
        "email" : "danieltest@cezar-trans.com",
        "company" : "Recruitment task",
        "website" : "www.google.pl",
        "country" : "Poland",
        "country_code" : "+48",
        "phone" : "555666777"
    }

    test = Ebook(account=details)
    test.get_url()

