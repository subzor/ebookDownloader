
import os
import requests
from ..Pages.EbooksPage import EbooksPage
from ..Tests.test_base import BaseTest
from ..Pages.LoginPage import LoginPage
from ..Config.config import TestData

class Test_LoginPage(BaseTest):
    """Class for test ebooks page"""

    def test_should_pass_when_country_is_not_correct(self):
        """Test for incorrect country selects"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        flag = login_page.select_country(TestData.INCORRECT_COUNTRY)

        assert not flag

    def test_should_pass_when_name_is_not_correct(self):
        """Test for incorrect name"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        try:
            login_page.chat_minimalise()
        except AttributeError as error:
            print(error)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.INCORRECT_NAME)
        login_page.click_download()

        assert login_page.check_error_visible(LoginPage.NAME_ERROR)

    def test_should_pass_when_email_is_not_correct(self):
        """Test for incorrect email"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.NAME)
        login_page.put_value(locator=LoginPage.EMAIL, value=TestData.INCORRECT_EMAIL)
        login_page.click_download()

        assert login_page.check_error_visible(LoginPage.EMAIL_ERROR)


    def test_should_pass_when_company_is_not_correct(self):
        """Test for incorrect company"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.NAME)
        login_page.put_value(locator=LoginPage.EMAIL, value=TestData.EMAIL)
        login_page.put_value(locator=LoginPage.COMPANY, value=TestData.INCORRECT_COMPANY)
        login_page.click_download()

        assert login_page.check_error_visible(LoginPage.COMPANY_ERROR)

    def test_should_pass_when_website_is_not_correct(self):
        """Test for incorrect website name"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.NAME)
        login_page.put_value(locator=LoginPage.EMAIL, value=TestData.EMAIL)
        login_page.put_value(locator=LoginPage.COMPANY, value=TestData.COMPANY)
        login_page.put_value(locator=LoginPage.WEBSITE, value=TestData.INCORRECT_WEBSITE)
        login_page.click_download()

        assert login_page.check_error_visible(LoginPage.WEBSITE_ERROR)


    def test_should_pass_when_phone_is_not_correct(self):
        """Test for incorrect phone number"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.NAME)
        login_page.put_value(locator=LoginPage.EMAIL, value=TestData.EMAIL)
        login_page.put_value(locator=LoginPage.COMPANY, value=TestData.COMPANY)
        login_page.put_value(locator=LoginPage.WEBSITE, value=TestData.WEBSITE)
        login_page.put_value(locator=LoginPage.PHONE, value=TestData.INCORRECT_PHONE)
        login_page.click_download()

        assert login_page.check_error_visible(LoginPage.PHONE_ERROR)


    def test_should_pass_when_move_to_thanks_page(self):
        """Test for correct inputs"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.NAME)
        login_page.put_value(locator=LoginPage.EMAIL, value=TestData.EMAIL)
        login_page.put_value(locator=LoginPage.COMPANY, value=TestData.COMPANY)
        login_page.put_value(locator=LoginPage.WEBSITE, value=TestData.WEBSITE)
        login_page.put_value(locator=LoginPage.PHONE, value=TestData.PHONE)
        login_page.select_country(TestData.COUNTRY)
        login_page.click_download()

        assert login_page.thanks_message_is_visible

    def test_should_pass_when_when_ebookExist(self):
        """Test for download ebook"""
        self.ebooksPage = EbooksPage(self.driver)
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        login_page = self.ebooksPage.go_to_url(correct_url)
        login_page.put_value(locator=LoginPage.NAME, value=TestData.NAME)
        login_page.put_value(locator=LoginPage.EMAIL, value=TestData.EMAIL)
        login_page.put_value(locator=LoginPage.COMPANY, value=TestData.COMPANY)
        login_page.put_value(locator=LoginPage.WEBSITE, value=TestData.WEBSITE)
        login_page.put_value(locator=LoginPage.PHONE, value=TestData.PHONE)
        login_page.select_country(TestData.COUNTRY)
        login_page.click_download()
        link = login_page.get_link_for_download_ebook()
        login_page.download_ebook(link)
        is_file = os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(__file__)),"download" ,TestData.EBOOK_NAME + ".pdf"))

        assert is_file