from threading import Thread
from queue import Queue
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


"""This class is parent of all pages"""
"""Contains all generic methods and utilities for all pages"""

class BasePage:

    def __init__(self, driver) -> None:
        self.driver = driver

    def do_click(self, by_locator: str) -> None:
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).click()
        # TODO change instances 

    def send_text(self, by_locator: str, text: str) -> None:
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def move_to_url(self, url) -> None:
        self.driver.get(url)

    def get_element_attribute(self, by_locator: str, attribute: str) -> str:
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).get_attribute(attribute)
        return element

    def get_all_elements(self, by_locator: str) -> list:
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(by_locator))
        return elements
    
    def is_visible(self, by_locator: str) -> bool:
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def get_title(self, title: str) -> str:
        WebDriverWait(self.driver, 10).until(EC.title_is(title))
        return self.driver.title

    def get_locator_text(self, by_locator: str) ->str:
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).text

    def select_by(self, by_locator: str, text_value: str) -> None:
        country_select = Select(WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)))
        try:
            country_select.select_by_visible_text(text_value)
        except Exception as error:
            print(error)
            return False


    def minimalise_chat(self, by_locator: str, minimise_button_class):
        try:
            chat_frame = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            self.driver.switch_to.frame(chat_frame)
            self.driver.find_element_by_class_name(minimise_button_class).click()
            self.driver.switch_to.default_content()
        except Exception as error:
            print(error)