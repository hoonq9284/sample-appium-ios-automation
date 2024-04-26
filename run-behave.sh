#!/bin/bash

# behave를 이용해 자동화 테스트를 수행하고, reports 디렉토리를 생성 후 테스트 기록을 하위에 저장
echo "Behave 자동화 테스트 수행 중..."
behave -f allure_behave.formatter:AllureFormatter -o reports/ features -f pretty

#export JAVA_HOME=/Library/Java/JavaVirtualMachines/adoptopenjdk-16.jdk/Contents/Home

# 테스트 완료 후 allure report 생성
echo "Allure 리포트 생성 중..."
allure generate reports/ -o allure-report/ --clean

# 생성된 allure report를 웹 서버를 통해 보기
echo "생성된 Allure 리포트 보기"
echo "Allure 리포트 검토 후, Ctrl + C 를 눌러 Web Server 종료"
allure serve reports

# 사용자 입력 대기 (Enter 키를 누르면 allure report가 종료되고, reports 디렉토리를 삭제함
read -p "리포트 검토 완료 후, Enter 키를 누르면 초기 상태로 복원"

# reports 디렉토리 삭제
rm -rf reports
echo "초기 상태로 복원 완료"