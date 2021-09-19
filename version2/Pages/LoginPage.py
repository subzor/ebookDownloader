
import os
import requests
from ..Config.config import TestData
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class LoginPage(BasePage):
    """By locators - OR"""
    """Class for login form page"""

    EBOKS = (By.XPATH, '//a[contains(text(),"Ebooks")]')
    NAME = (By.NAME, "name")
    EMAIL = (By.ID, "email")
    COMPANY = (By.NAME, "company")
    WEBSITE = (By.NAME, "url") 
    COUNTRY = (By.ID, "countryOptions") 
    PHONE = (By.ID, "phoneNumber") 
    CLICK_BUTTON = (By.XPATH, '//*[@class="fa fa-angle-right fa-lg"]')
    THANKS_MASSAGE = (By.CLASS_NAME , "thanks-message")
    DOWNLOAD_BUTTON = (By.XPATH, '//a[contains(text(),"HERE")]')
    CHAT = (By.CLASS_NAME, "bhr-chat__messenger")
    MINIMALISE_CHAT = "bhr-chat-messenger__minimalise"

    NAME_ERROR = (By.ID , "name-error")
    EMAIL_ERROR = (By.ID, "email-error")
    COMPANY_ERROR = (By.ID, "company-error")
    WEBSITE_ERROR = (By.ID, "url-error")
    PHONE_ERROR = (By.XPATH, '//*[@class="error diallingCode-error"]')

    def __init__(self, driver) -> None:
        super().__init__(driver)
        """Constructor of the page"""

    def put_value(self, locator: str, value: str) -> None:
        """Send text to webpage element"""
        self.send_text(locator, value)

    def click_download(self) -> None:
        """Click on webpage element"""
        self.do_click(LoginPage.CLICK_BUTTON)

    def chat_minimalise(self) -> None:
        """Minimalise chat from webpage"""
        self.minimalise_chat(LoginPage.CHAT, LoginPage.MINIMALISE_CHAT)
        
    def check_error_visible(self, locator: str) -> bool:
        """Check if input error occured"""
        return self.is_visible(locator)

    def select_country(self, value: str)  -> bool:
        """Select country from dropdown list"""
        flag = self.select_by(LoginPage.COUNTRY, value)
        return flag

    def thanks_message_is_visible(self) -> bool:
        """Check if thanks iframe is visible"""
        return self.is_visible(LoginPage.THANKS_MASSAGE)

    def get_link_for_download_ebook(self) -> str:
        """Retrieve link from webpage element"""
        return self.get_element_attribute(LoginPage.DOWNLOAD_BUTTON, "href")

    def download_ebook(self, link: str) -> None:
        """Download ebook"""
        r = requests.get(link, allow_redirects=True)
        open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "download", TestData.EBOOK_NAME + ".pdf"), 'wb').write(r.content)
