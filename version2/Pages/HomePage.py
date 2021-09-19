
from version2.Config.config import TestData
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class HomePage(BasePage):
    """By locators - OR"""
    """Class for startig page"""

    BURGER_MENU = (By.ID, "nav-toggler")
    RESOURCES = (By.XPATH, '//a[contains(text(),"resources")]')
    EBOKS = (By.XPATH, '//a[contains(text(),"Ebooks")]')

    def __init__(self, driver) -> None:
        super().__init__(driver)
        """Constructor of the page"""

        self.driver.get(TestData.BASE_URL)

    def get_home_page_title(self, title: str) -> str:
        """Used to get the title from page"""
        return self.get_title(title)
    
    def is_burger_menu_exist(self) -> bool:
        """Check is burger menu exist"""
        return self.is_visible(self.BURGER_MENU)

    def go_to_ebooks_page(self) -> None:
        """Go to next page method"""
        self.do_click(self.BURGER_MENU)
        self.do_click(self.RESOURCES)
        self.do_click(self.EBOKS)
