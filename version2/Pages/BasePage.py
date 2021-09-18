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

    def select_by(self, by_locator: str, country) -> None:
        country_select = Select(self.driver.find_element_by_id("countryOptions"))
        country_select.select_by_visible_text(country)