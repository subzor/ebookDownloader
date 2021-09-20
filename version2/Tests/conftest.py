import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ..Config.config import TestData

@pytest.fixture(params=["chrome"], scope="class")
def init_driver(request):
    """Initialize friver"""
    if request.param == "chrome":
        options = ChromeOptions()
        options.add_argument("--width=1300")
        options.add_argument("--height=1000")
        web_driver = webdriver.Chrome(executable_path=TestData.CHROME_EXECUTABLE_PATH, options=options)
    if request.param == "firefox":
        web_driver = webdriver.Firefox(executable_path=TestData.FIREFOX_EXECUTABLE_PATH)
    
    request.cls.driver = web_driver
    yield
    web_driver.close()
