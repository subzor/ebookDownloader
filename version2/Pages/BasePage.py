from threading import Thread
from queue import Queue
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class BasePage:
    """This class is parent of all pages"""
    """Contains all generic methods and utilities for all pages"""

    def __init__(self, driver) -> None:
        """Constructor of the page"""
        self.driver = driver
        self.web_driver = WebDriverWait(self.driver, 10)

    def do_click(self, by_locator: str) -> None:
        """Do click on webpage object"""
        self.web_driver.until(EC.visibility_of_element_located(by_locator)).click()

    def send_text(self, by_locator: str, text: str) -> None:
        """Send text to webpage object"""
        self.web_driver.until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def move_to_url(self, url: str) -> None:
        """Move to specific url"""
        self.driver.get(url)

    def get_element_attribute(self, by_locator: str, attribute: str) -> str:
        """Get attribute from webpage object"""
        element = self.web_driver.until(EC.visibility_of_element_located(by_locator)).get_attribute(attribute)
        return element

    def get_all_elements(self, by_locator: str) -> list:
        """Get all elements from webpage object"""
        elements = self.web_driver.until(EC.visibility_of_all_elements_located(by_locator))
        return elements
    
    def is_visible(self, by_locator: str) -> bool:
        """Check is webpage object is visible"""
        try:
            element = self.web_driver.until(EC.visibility_of_element_located(by_locator))
        except Exception as error:
            print(error)
            element = False
        return bool(element)

    def get_title(self, title: str) -> str:
        """Get webpage title"""
        self.web_driver.until(EC.title_is(title))
        return self.driver.title

    def get_locator_text(self, by_locator: str) ->str:
        """Get text from webpage object"""
        return self.web_driver.until(EC.visibility_of_element_located(by_locator)).text

    def select_by(self, by_locator: str, text_value: str) -> bool:
        """Select webpage object from dropdown list"""
        country_select = self.web_driver.until(EC.visibility_of_element_located(by_locator))
        try:
            country_select.select_by_visible_text(text_value)
        except Exception as error:
            print(error)
            return False
        return True

    def minimalise_chat(self, by_locator: str, minimise_button_class: str) -> None:
        """Minimalise live chat"""
        try:
            chat_frame = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            self.driver.switch_to.frame(chat_frame)
            self.driver.find_element_by_class_name(minimise_button_class).click()
            self.driver.switch_to.default_content()
        except Exception as error:
            print(error)
