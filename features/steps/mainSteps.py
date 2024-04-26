from behave import when, then


@when('네이버 알림 팝업을 닫는다.')
def step_impl(context):
    context.mp.close_naver_noti_modal()


@when('네이버 URL 에 접속한다.')
def step_impl(context):
    context.mp.input_naver_keyword()


@when('네이버 검색 결과를 터치한다.')
def step_impl(context):
    context.mp.touch_naver_search_result()
