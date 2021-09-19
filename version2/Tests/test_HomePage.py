
from ..Config.config import TestData
from ..Pages.HomePage import HomePage
from ..Tests.test_base import BaseTest

class Test_HomePage(BaseTest):
    """Class for test startig page"""

    # TODO Change names of tests 
    def test_should_pass_when_burger_menu_is_visible(self):
        """Burger menu test"""
        self.homePage = HomePage(self.driver)
        menu = self.homePage.is_burger_menu_exist()
        assert menu

    def test_should_pass_when_home_page_title_is_correct(self):
        """Web title test"""
        self.homePage = HomePage(self.driver)
        title = self.homePage.get_home_page_title(TestData.HOME_PAGE_TITLE)
        assert title == TestData.HOME_PAGE_TITLE

    def test_should_pass_when_next_page_title_is_correct(self):
        """Test for step to another page"""
        self.homePage = HomePage(self.driver)
        self.homePage.go_to_ebooks_page()
        title = self.homePage.get_home_page_title(TestData.SECOND_PAGE_TITLE)
        assert title == TestData.SECOND_PAGE_TITLE
