import pages.PageElements as pe
import utilities.CustomLogger as cl
from base.BasePage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
import time


class MainPage(BasePage):

    def __init__(self, driver, context):
        super().__init__(driver, context)
        self.driver = driver
        self.context = context
        self.url = "naver.com"
        self.text = "네이버 항공권"

    def input_naver_keyword(self):
        BasePage.send_key_element(self, AppiumBy.XPATH, pe.safari_url_field, self.url)
        cl.allure_logs("Safari 에 naver url 검색")

    def touch_naver_search_result(self):
        BasePage.touch_element(self, AppiumBy.XPATH, pe.safari_naver_search_result)
        cl.allure_logs("Safari naver 검색 결과 터치")
