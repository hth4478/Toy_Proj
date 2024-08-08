from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_job_data(query):
    # ChromeOptions 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음

    # ChromeDriver 경로 설정
    chrome_driver_path = r'C:\workspace_toyProj\chromedriver-win64\chromedriver.exe'

    # Service 객체 생성 후 WebDriver 초기화
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # JobKorea 페이지 로드
    driver.get(f'https://www.jobkorea.co.kr/Search/?stext={query}')

    # 페이지 소스를 BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 브라우저 종료
    driver.quit()

    job_list = []

    # main-wrap 안의 article 태그 선택
    main_wrap = soup.find('div', class_='main-wrap')
    if not main_wrap:
        print("main-wrap not found")
        return []
    
    # main-wrap 안의 article 태그에서 list 클래스가 있는 태그를 먼저 찾음
    list_wrap = main_wrap.find('article', class_='list')
    if not list_wrap:
        print("list article not found")
        return []

    # 상위 10개 가져오기
    # job_elements = list_wrap.find_all('div', class_='list-section-information')[:10]
    job_elements = list_wrap.find_all('article')[:10]

    # job_elements = main_wrap.find_all('article', class_='list')[:10]  # 상위 10개 데이터 가져오기
    
    print(f"Found {len(job_elements)} job elements")  # 가져온 요소의 개수 출력

    for index, job_element in enumerate(job_elements):
        print(f"Processing job element {index + 1}/{len(job_elements)}")  # 디버깅용

        # 회사명 추출
        company_elem = job_element.select_one('div.list-section-corp a')
        if not company_elem:
            print("Company element not found")
            continue
        company = company_elem.text.strip()

        # 공고 제목과 링크 추출
        title_elem = job_element.select_one('div.information-title a')
        if not title_elem:
            print("Title element not found")
            continue
        title = title_elem.text.strip()
        link = 'https://www.jobkorea.co.kr' + title_elem['href']

        job_list.append({
            'company': company,
            'title': title,
            'link': link
        })
    
    return job_list

# 예시 사용법
query = '데이터분석'
jobs = get_job_data(query)

for job in jobs:
    print(f"회사명: {job['company']}")
    print(f"제목: {job['title']}")
    print(f"링크: {job['link']}")
    print('-' * 20)
