import pytest
import time
from ..Pages.HomePage import HomePage
from ..Pages.EbooksPage import EbooksPage
from ..Tests.test_base import BaseTest
from ..Pages.LoginPage import LoginPage
from ..Config.config import TestData
from selenium.webdriver.common.by import By

class Test_LoginPage(BaseTest):


    def test_should_pass_when_name_is_not_correct(self):
        self.homePage = HomePage(self.driver)
        self.ebooksPage = self.homePage.go_to_ebooks_page()
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.chat_minimalise()
        login_page.click_download()
        login_page.put_incorrect_value(locator=LoginPage.NAME, incorrect_value=TestData.INCORRECT_NAME)

        assert login_page.check_error_visible(LoginPage.NAME_ERROR)


    def test_should_pass_when_email_is_not_correct(self):
        self.homePage = HomePage(self.driver)
        self.ebooksPage = self.homePage.go_to_ebooks_page()
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.chat_minimalise()
        login_page.click_download()
        login_page.put_incorrect_value(locator=LoginPage.NAME, incorrect_value=TestData.NAME)
        login_page.put_incorrect_value(locator=LoginPage.EMAIL, incorrect_value=TestData.INCORRECT_EMAIL)

        assert login_page.check_error_visible(LoginPage.EMAIL_ERROR)


    def test_should_pass_when_country_is_not_correct(self):
        self.homePage = HomePage(self.driver)
        self.ebooksPage = self.homePage.go_to_ebooks_page()
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.chat_minimalise()
        login_page.click_download()
        login_page.put_incorrect_value(locator=LoginPage.NAME, incorrect_value=TestData.NAME)
        login_page.put_incorrect_value(locator=LoginPage.EMAIL, incorrect_value=TestData.EMAIL)
        flag = login_page.select_country()

        assert flag