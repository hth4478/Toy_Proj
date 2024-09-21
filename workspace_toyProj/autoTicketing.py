from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
import requests

# 서버 시간 확인을 위한 함수 (헤더에서 날짜 추출 가정)
def get_server_time(url):
    response = requests.head(url)  # 서버 시간은 헤더에서 가져온다고 가정
    server_time = response.headers['Date']  # 헤더에서 'Date' 필드 사용
    server_time = datetime.strptime(server_time, '%a, %d %b %Y %H:%M:%S %Z')
    return server_time

# 타겟 URL 실행 함수
def execute_url(target_url, target_time):
    print(f"지정된 URL 실행: {target_url}")
    response = requests.get(target_url)
    print(f"응답 상태 코드: {response.status_code}")
    if(response.status_code == 200):
        try:
            # 브라우저 옵션 설정 (백그라운드에서 실행하려면 headless 모드 사용 가능)
            chrome_options = Options()
            # chrome_options.add_argument("--headless")  # GUI 없이 실행하고 싶다면 이 줄을 활성화

            # ChromeDriver 경로 설정
            chrome_driver_path = r'C:\workspace_toyProj\chromedriver-win64\chromedriver.exe'
            # WebDriver 실행 경로 설정
            webdriver_service = Service(executable_path=chrome_driver_path)

            # 브라우저 실행
            driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

            # 지정된 URL로 접속
            driver.get(target_url)

            # 로그인
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "header_util_link"))
            ).click()

            # 새 브라우저 창으로 전환
            original_window = driver.current_window_handle
            new_window = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_window)

            id_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id"))
            )
            pw_input = driver.find_element(By.ID, "pw")
            login_btn = driver.find_element(By.ID, "loginBtn")

            # ID와 비밀번호 입력 (여기에 실제 값 입력)
            id_input.send_keys("taehwan4478@naver.com")
            pw_input.send_keys("Xoghks4478!")

            # 로그인 버튼 클릭
            login_btn.click()

            # 로그인 완료 후 현재 시간을 추적
            print("로그인 완료, 서버 시간이 지정된 시간에 도달할 때까지 대기 중...")

            while True:
                server_time = get_server_time(target_url)
                print(f"현재 서버 시간: {server_time}")

                if server_time >= target_time:
                    # "match_btn" 클래스를 가진 <div> 요소를 기다리고 찾기
                    match_btn_div = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "match_btn"))
                    )
                    
                    # "match_btn" 하위의 "btn btn_reserve" 클래스를 가진 <a> 요소를 찾기
                    reserve_button = match_btn_div.find_element(By.CSS_SELECTOR, "a.btn.btn_reserve")
                    
                    # 버튼 클릭
                    reserve_button.click()
                    print("버튼이 성공적으로 클릭되었습니다.")
                    break

                # 서버 시간이 지정된 시간까지 대기
                time.sleep(5)

                # 현재 시간에서 3분이 지난 경우 브라우저 종료
                if datetime.now() > (server_time + timedelta(minutes=3)):
                    print("지정된 시간에서 3분이 지나 브라우저를 종료합니다.")
                    driver.quit()
                    break

        except Exception as e:
            print(f"예외 발생: {e}")
            driver.quit()

# 예시 사용법
target_url = "https://www.ticketlink.co.kr/sports/baseball/58#reservation"  # 지정된 시간이 되면 실행할 URL
target_time = datetime(2024, 9, 9, 9, 28, 0)  # 지정된 시간 (예시)

# 함수 실행
execute_url(target_url, target_time)
