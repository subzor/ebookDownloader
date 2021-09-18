from .EbooksPage import EbooksPage
from version2.Config.config import TestData
from selenium.webdriver.common.by import By
import sys

from .BasePage import BasePage


class HomePage(BasePage):

    """By locators - OR"""
    BURGER_MENU = (By.ID, "nav-toggler")
    RESOURCES = (By.XPATH, '//a[contains(text(),"resources")]')
    EBOKS = (By.XPATH, '//a[contains(text(),"Ebooks")]')

    """Constructor of the page"""
    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL)

    """Used to get the title from page"""
    def get_home_page_title(self, title: str) -> str:
        return self.get_title(title)
    
    """Check is burger menu exist"""
    def is_burger_menu_exist(self) -> bool:
        return self.is_visible(self.BURGER_MENU)

    """Go to next page method"""
    def go_to_ebooks_page(self):
        self.do_click(self.BURGER_MENU)
        self.do_click(self.RESOURCES)
        self.do_click(self.EBOKS)
        return self.driver



    