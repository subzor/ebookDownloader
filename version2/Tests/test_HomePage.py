
from ..Config.config import TestData
import pytest

from ..Pages.HomePage import HomePage
from ..Tests.test_base import BaseTest

class Test_HomePage(BaseTest):

    # TODO Change names of tests 
    def test_burger_menu_is_visible(self):
        self.homePage = HomePage(self.driver)
        flag = self.homePage.is_burger_menu_exist()
        assert flag

    def test_home_page_title(self):
        self.homePage = HomePage(self.driver)
        title = self.homePage.get_home_page_title(TestData.HOME_PAGE_TITLE)
        assert title == TestData.HOME_PAGE_TITLE

    def test_go_to_next_page(self):
        self.homePage = HomePage(self.driver)
        self.homePage.go_to_ebooks_page()

    def test_next_page_title(self):
        self.homePage = HomePage(self.driver)
        self.homePage.go_to_ebooks_page()
        title = self.homePage.get_home_page_title(TestData.SECOND_PAGE_TITLE)
        assert title == TestData.SECOND_PAGE_TITLE
        