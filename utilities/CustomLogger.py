import logging
import os
import allure


def allure_logs(text):
    """
    allure 리포트에 테스트 케이스 로그 메시지를 기록하는 함수
    :param text:
    :return:
    """
    with allure.step(text):
        pass


def custom_logger(name):
    """
    Test_log.log 파일을 reports 디렉토리 하위에 생성하고, 로그 기록을 지원하는 함수
    :param name:
    :return:
    """
    log_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "test_error_log.log")

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
