from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class OneVisitorTest(LiveServerTestCase):
    """one visitor test"""

    def setUp(self):
        """instalation"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """demontaj"""
        self.browser.quit()
