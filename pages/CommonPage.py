from base.BasePage import BasePage
import pages.PageElements as pe
from appium.webdriver.common.appiumby import AppiumBy


class CommonPage(BasePage):

    def __init__(self, driver, context):
        super().__init__(driver, context)
        self.driver = driver
        self.context = context
