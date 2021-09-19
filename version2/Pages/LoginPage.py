
from .EbooksPage import EbooksPage
from .HomePage import HomePage
from version2.Config.config import TestData
from selenium.webdriver.common.by import By
import sys

from .BasePage import BasePage


class LoginPage(BasePage):

    """By locators - OR"""
    NAME = (By.NAME, "name")
    EMAIL = (By.ID, '"email"')
    EBOKS = (By.XPATH, '//a[contains(text(),"Ebooks")]')
    COMPANY = (By.NAME, "company")
    WEBSITE = (By.NAME, "url") 
    COUNTRY = (By.ID, "countryOptions") 
    PHONE = (By.ID, "phoneNumber") 
    CLICK_BUTTON = (By.XPATH, '//*[@class="fa fa-angle-right fa-lg"]')

    CHAT = (By.CLASS_NAME, "bhr-chat__messenger")
    MINIMALISE_CHAT = "bhr-chat-messenger__minimalise"

    NAME_ERROR = (By.ID , "name-error")
    EMAIL_ERROR = (By.ID, "email-error")
    COMPANY_ERROR = (By.ID, "company-error")
    WEBSITE_ERROR = (By.ID, "url-error")
    PHONE_EMPTY_ERROR = (By.ID, "phoneNumber-error")
    PHONE_ERROR = (By.CLASS_NAME, "error diallingCode-error")


    """Constructor of the page"""
    def __init__(self, driver) -> None:
        super().__init__(driver)
        
    def put_incorrect_value(self, locator ,incorrect_value):
        self.send_text(locator, incorrect_value)

    def put_correct_value(self, locator, correct_value):
        self.send_text(locator, correct_value)

    def click_download(self):
        self.do_click(LoginPage.CLICK_BUTTON)

    def chat_minimalise(self):
        self.minimalise_chat(LoginPage.CHAT, LoginPage.MINIMALISE_CHAT)
        
    def check_error_visible(self, locator):
        return self.is_visible(locator)

    def select_country(self):
        flag = self.select_by(LoginPage.COUNTRY, TestData.INCORRECT_COUNTRY)
        return flag
