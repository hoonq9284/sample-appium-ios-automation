from base.BasePage import BasePage
from pages.CommonPage import CommonPage
from pages.MainPage import MainPage
from behave import given


@given('테스트 수행 전 초기화한다.')
def step_impl(context):
    context.bs = BasePage(context.driver, context)
    context.cp = CommonPage(context.driver, context)
    context.mp = MainPage(context.driver, context)
