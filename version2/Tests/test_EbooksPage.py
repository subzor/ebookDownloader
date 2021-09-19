
import pytest
import time
from ..Pages.HomePage import HomePage
from ..Tests.test_base import BaseTest
from ..Config.config import TestData

class Test_EbooksPage(BaseTest):

    def test_should_pass_when_list_of_url_are_not_empty(self):
        self.homePage = HomePage(self.driver)
        self.ebooksPage = self.homePage.go_to_ebooks_page()
        list_of_links = self.ebooksPage.get_all_links()
        print(list_of_links)
        assert (isinstance(list_of_links, list) and (len(list_of_links) > 0 ))


    def test_should_pass_when_move_to_correct_ebook(self):
        self.homePage = HomePage(self.driver)
        self.ebooksPage = self.homePage.go_to_ebooks_page()
        list_of_links = self.ebooksPage.get_all_links()
        correct_url = self.ebooksPage.get_url_from_thread(list_of_links=list_of_links, ebook_name=TestData.EBOOK_NAME)
        print(correct_url)
        self.ebooksPage.go_to_url(correct_url)
        assert TestData.EBOOK_NAME in self.ebooksPage.driver.title