
from .EbooksPage import EbooksPage
from version2.Config.config import TestData
from selenium.webdriver.common.by import By
import sys

from .BasePage import BasePage


class HomePage(BasePage):

    """By locators - OR"""
    NAME = (By.NAME, "name")
    EMAIL = (By.ID, '"email"')
    EBOKS = (By.XPATH, '//a[contains(text(),"Ebooks")]')
    COMPANY = (By.NAME, "company")
    WEBSITE = (By.NAME, "url") 
    COUNTRY = (By.ID, "countryOptions") 
    PHONE = (By.ID, "phoneNumber") 
