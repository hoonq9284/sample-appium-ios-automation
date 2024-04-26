import os
import allure
import time
import io
import config.config as config
import utilities.helper as helper
import utilities.CustomLogger as log

from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.common.exceptions import *
from appium.webdriver.common.touch_action import TouchAction

from allure_commons.types import AttachmentType
from PIL import Image, ImageDraw
from traceback import print_stack

# 전역 변수 목록
waitTime = config.WAIT_TIME
BASE_DIR = os.getcwd()
logger = log.custom_logger(name=__name__)
image_scale_numeric = config.IMAGE_SCALE_NUMERICAL


class BasePage:

    def __init__(self, driver, context):
        self.driver = driver
        self.context = context

    def touch_screen_center(self):
        width, height = helper.get_screen_size(self.driver)
        x = width / 2
        y = height / 2
        TouchAction(self.driver).tap(x=x, y=y).perform()

    def write_log(self, locator, text):
        """
        로그 및 스크린샷을 기록하는 메서드
        :param locator:
        :param text:
        :return:
        """
        print_stack()
        logger.info(locator + text)
        self.take_screenshot_allure(locator)
        self.save_screenshot_to_file()

    def save_screenshot_to_file(self, prefix='screenshot', suffix=''):
        """
        웹 페이지의 스크린샷을 저장하고, 이미지 이름 포맷 지정 및 해당 파일 경로를 반환하는 메서드
        :param prefix: 파일명 앞에 붙일 텍스트
        :param suffix: 파일명 뒤에 붙일 텍스트
        :return: (Image object, image file path)
        """
        # 파일명 형식: "screenshot_20220424_120705.png"
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        image_file_name = f"{prefix}_{timestamp}{suffix}.png"
        image_file_path = os.path.join(BASE_DIR, "reports", image_file_name)

        self.driver.save_screenshot(image_file_path)
        image = Image.open(image_file_path)
        logger.info(f'{image_file_path} : 저장됨')

        # # 이미지 크기 및 압축 설정
        # image = Image.open(image_file_path)
        # 이미지 크기를 image_scale_numeric 만큼의 %로 축소 (필요에 따라 조정)
        # image = image.resize(
        #     (
        #         int(
        #             image.width * image_scale_numeric
        #         ), int(
        #             image.height * image_scale_numeric
        #         )
        #     ), Image.Resampling.LANCZOS
        # )
        # # 이미지 압축
        # image.save(image_file_path, 'PNG', quality=85)
        # logger.info(f'{image_file_path} : 저장됨')
        return image, image_file_path

    def take_screenshot_allure(self, text):
        """
        스크린샷을 저장하고, allure 리포트에 첨부하는 메서드
        :param text:
        :return:
        """
        # 원본 스크린샷을 PNG 형태로 바이트 배열로 가져옴
        raw_image = self.driver.get_screenshot_as_png()

        # Pillow를 사용하여 이미지 객체로 변환
        image = Image.open(io.BytesIO(raw_image))

        # 이미지 크기를 image_scale_numeric 만큼의 %로 축소 (필요에 따라 조정)
        resized_image = image.resize(
            (
                int(
                    image.width * image_scale_numeric
                ), int(
                    image.height * image_scale_numeric
                )
            ), Image.Resampling.LANCZOS
        )

        # 조정된 이미지를 바이트 배열로 다시 변환
        byte_array = io.BytesIO()
        resized_image.save(byte_array, format='PNG')

        allure.attach(byte_array.getvalue(), name=text, attachment_type=AttachmentType.PNG)

    @staticmethod
    def attach_image_to_allure(file_path, description):
        """
        파일 경로에서 이미지를 읽어 Allure 리포트에 첨부하는 메서드
        :param file_path: 이미지 파일의 경로
        :param description: 첨부할 이미지에 대한 설명
        """
        with open(file_path, "rb") as image_file:
            allure.attach(image_file.read(), name=description, attachment_type=AttachmentType.PNG)

    def highlight(self, element, color, border, scale_factor=image_scale_numeric):
        """
        스크린샷을 찍고, 이미지 크기를 줄인 후 해당 크기에 맞춰 하이라이트 적용
        :param element: 포커스 할 요소
        :param color: 테두리 효과 컬러 코드
        :param border: 테두리 굵기
        :param scale_factor: 이미지 크기 조정 비율
        :return:
        """
        image, screenshot_path = self.save_screenshot_to_file()

        # 이미지 크기 조정
        resized_image = image.resize((int(image.width * scale_factor), int(image.height * scale_factor)),
                                     Image.Resampling.LANCZOS)

        # 요소의 위치 및 크기 조정
        location = element.location
        size = element.size
        scaled_left = int(location['x'] * scale_factor)
        scaled_top = int(location['y'] * scale_factor)
        scaled_right = scaled_left + int(size['width'] * scale_factor)
        scaled_bottom = scaled_top + int(size['height'] * scale_factor)

        # 조정된 위치에 하이라이트 적용
        draw = ImageDraw.Draw(resized_image)
        draw.rectangle([scaled_left, scaled_top, scaled_right, scaled_bottom], outline=color,
                       width=int(border * scale_factor))

        # 변경된 이미지 저장
        resized_image.save(screenshot_path)

        # Allure 리포트에 변경된 이미지 첨부
        self.attach_image_to_allure(screenshot_path, "screenshot")

    def app_element_wait(self, by_selector, locator):
        try:
            WebDriverWait(self.driver, waitTime).until(
                EC.presence_of_element_located((by_selector, locator))
            )
        except TimeoutException:
            print_stack()
            assert False

    def is_displayed(self, by_selector, locator):
        try:
            self.app_element_wait(by_selector, locator)
            element = self.driver.find_element(by=by_selector, value=locator)
            element.is_displayed()
            self.highlight(element, "#ff0000", 10)
            return True
        except NoSuchElementException:
            print_stack()
            assert False

    def touch_element(self, by_selector, locator):
        try:
            self.app_element_wait(by_selector, locator)
            element = self.driver.find_element(by=by_selector, value=locator)
            self.highlight(element, "#ff0000", 10)
            element.click()
            return True
        except NoSuchElementException:
            print_stack()
            assert False

    def send_key_element(self, by_selector, locator, text):
        try:
            self.app_element_wait(by_selector, locator)
            element = self.driver.find_element(by=by_selector, value=locator)
            element.send_keys(text)
            self.highlight(element, "#ff0000", 10)
            return True
        except NoSuchElementException:
            print_stack()
            assert False

    def get_element_text(self, by_selector, locator):
        self.app_element_wait(by_selector, locator)
        try:
            element = self.driver.find_element(by=by_selector, value=locator)
            text = element.text
            return text
        except NoSuchElementException:
            print_stack()
            assert False

    def terminate_app(self):
        self.driver.terminate_app(config.BUNDLE_ID)

    def activate_app(self):
        self.driver.activate_app(config.BUNDLE_ID)
