
import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

from ..Config.config import TestData


from selenium.webdriver.common.by import By
import sys

from .BasePage import BasePage



class EbooksPage(BasePage):

    EBOOKS_LINKS = (By.XPATH, '//*[@class="ebook__img--container"]//a')

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def go_to_url(self, url):
        self.driver.get(url)
        from .LoginPage import LoginPage
        lol = LoginPage(self.driver)
        return lol


    def get_all_links(self):
        list_of_links = []
        ebooks_list = self.get_ebooks_list()
         
        if ebooks_list:
            for ebook in ebooks_list:
                list_of_links.append(ebook.get_attribute("href"))
        
        return list_of_links

    def get_ebooks_list(self):
        s = self.get_all_elements(self.EBOOKS_LINKS)
        return s


    def get_url_from_thread(self, list_of_links, ebook_name):
        que = Queue()

        thread_list = []

        for url in list_of_links:
            worker = Thread(target=self.__get_ebook_name, args=(que, url, ebook_name))
            thread_list.append(worker)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        return que.get()



    def __get_ebook_name(self, que, url, ebook_name):

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
        
        name = soup.title.string

        if ebook_name in name:
            que.put(url)

            