import json
import os
import datetime
import pytz


def get_screen_size(driver):
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    return width, height


def create_json(data, filename):
    """
    데이터를 JSON 형식으로 직렬화하여 파일에 저장
    :param data: JSON으로 변환할 데이터
    :param filename: 저장할 파일명
    """
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def delete_json_file(filename):
    """
    지정된 파일을 삭제
    :param filename: 삭제할 파일명
    """
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} 파일이 삭제되었습니다.")
    else:
        print(f"{filename} 파일이 존재하지 않습니다.")


def get_current_time():
    """
    현재 시각 구하는 함수
    :return:
    """
    seoul_tz = pytz.timezone('Asia/Seoul')
    # 서울 시간대의 현재 시각을 얻음
    current_time = datetime.datetime.now(seoul_tz)
    return current_time
