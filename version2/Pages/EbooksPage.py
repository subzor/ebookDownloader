
import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from selenium.webdriver.common.by import By

from ..Config.config import TestData
from .HomePage import HomePage
from .BasePage import BasePage

class EbooksPage(BasePage):
    """By locators - OR"""
    """Class for page with all ebooks"""

    EBOOKS_LINKS = (By.XPATH, '//*[@class="ebook__img--container"]//a')

    def __init__(self, driver) -> None:
        super().__init__(driver)
        """Constructor of the page"""

        self.driver.get(TestData.BASE_URL)
        if self.is_visible(HomePage.COOCKIES):
            try:
                self.do_click(HomePage.COOCKIES)
            except AttributeError as error:
                print(error)
        if self.is_visible(HomePage.CHAT):
            try:
                self.minimalise_chat(HomePage.CHAT, HomePage.MINIMALISE_CHAT)
            except AttributeError as error:
                print(error)
        self.do_click(HomePage.BURGER_MENU)
        self.do_click(HomePage.RESOURCES)
        self.do_click(HomePage.EBOKS)

    def go_to_url(self, url: str) -> object:
        """Used to move to specific ebook and pass driver to another page"""
        self.driver.get(url)
        from .LoginPage import LoginPage
        return LoginPage(self.driver)

    def get_all_links(self) ->list:
        """Retrieve links from Selenium webelements"""
        list_of_links = []
        ebooks_list = self.get_ebooks_list()
         
        if ebooks_list:
            for ebook in ebooks_list:
                list_of_links.append(ebook.get_attribute("href"))
        
        return list_of_links

    def get_ebooks_list(self) ->list:
        """Used to retrieve all element located by* from webpage"""
        return self.get_all_elements(self.EBOOKS_LINKS)


    def get_url_from_thread(self, list_of_links: list, ebook_name: str) -> str:
        """Used to pass ebooks links to check correctness"""
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

    def __get_ebook_name(self, que: object, url: str, ebook_name: str) -> str:
        """Used to retrieve link to correct ebook"""
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
