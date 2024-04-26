import os
import config.config as config
import utilities.helper as helper

from appium import webdriver
from appium.webdriver.appium_service import AppiumService


# 전역 변수 목록
appium_service = AppiumService()
BASE_DIR = os.getcwd()
URL = config.URL
apps = config.APP_FILE
app = os.path.join(BASE_DIR, 'apps', apps)
start_time = None
end_time = None
scenario_test_results = []

print("Base Dir : " + BASE_DIR)
print("App Path : " + app)


def before_all(context):
    global start_time
    appium_service.start()
    print("==================== appium service started ====================")
    capabilities = {
        # "app": app,
        "platformName": config.PLATFORM_NAME,
        "appium:platformVersion": config.PLATFORM_VERSION,
        "appium:automationName": config.AUTOMATION_NAME,
        "appium:udid": config.UDID,
        "bundleId": config.BUNDLE_ID,
        # "appium:xcodeOrgId": config.XCODE_ORG_ID
        # "appium:xcodeSigningId": "iPhone Developer"
        "autoAcceptAlerts": "true",
        "autoGrantPermissions": "true",
        "disableWindowAnimation": "true",
    }

    context.driver = webdriver.Remote(command_executor=URL, desired_capabilities=capabilities)
    helper.delete_json_file("test_result.json")
    start_time = helper.get_current_time()


def before_feature(context, feature):
    global start_time
    start_time = helper.get_current_time()
    print("===" + feature.filename + " : 테스트 시작" + "===")


def before_scenario(context, scenario):
    scenario_info = {
        "name": scenario.name,
        "status": "unknown"
    }
    scenario_test_results.append(scenario_info)


def after_scenario(context, scenario):
    for scenario_info in scenario_test_results:
        if scenario_info["name"] == scenario.name:
            scenario_info["status"] = scenario.status.name
    helper.create_json(scenario_test_results, "test_result.json")


def after_feature(context, feature):
    global start_time, end_time
    end_time = helper.get_current_time()
    time_required = end_time - start_time
    minutes, seconds = divmod(time_required.seconds, 60)
    feature_name = feature.filename
    formatted_time = f"{minutes}분 {seconds}초"
    print(f"=== {feature_name} 테스트 종료 ===")
    print(f"=== {feature_name} 테스트 소요 시간 : {formatted_time} ===")


def after_all(context):
    context.driver.quit()
    appium_service.stop()
    print("==================== appium service stopped ====================")
