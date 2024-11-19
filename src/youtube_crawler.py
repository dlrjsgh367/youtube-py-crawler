import time
from tempfile import mkdtemp
import signal
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from download_youtube_video import download_youtube_video

def signal_handler(sig, frame):
    print("\n프로그램이 강제 종료되었습니다.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def web_driver_options():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280x1696')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-dev-tools')
    options.add_argument('--no-zygote')
    options.add_argument(f'--user-data-dir={mkdtemp()}')
    options.add_argument(f'--data-path={mkdtemp()}')
    options.add_argument(f'--disk-cache-dir={mkdtemp()}')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    return options

def create_web_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=web_driver_options())

def scroll_until_end(driver, max_scroll_attempts=1000):
    scroll_count = 0
    while scroll_count < max_scroll_attempts:
        try:
            driver.find_element(By.XPATH, '//*[@id="message"]')
            break
        except NoSuchElementException:
            driver.execute_script('window.scrollBy(0, 1000);')
            scroll_count += 1
        time.sleep(1)  # 로딩이 제대로 이루어지도록 약간의 지연 시간을 추가

def extract_video_links(driver, max_sections=40, max_contents=20):
    video_links = []
    for section_idx in range(1, max_sections + 1):
        for content_idx in range(1, max_contents + 1):
            try:
                content = driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{section_idx}]/div[3]/ytd-video-renderer[{content_idx}]')
                link = content.find_element(By.ID, 'thumbnail').get_attribute('href')
                if link and ('/watch?v=' in link or '/shorts/' in link):
                    video_links.append(link)
            except NoSuchElementException:
                continue
    return video_links

def main(keyword):
    url = f'https://www.youtube.com/results?search_query={keyword}'
    driver = create_web_driver()
    driver.get(url)
    
    try:
        # "동영상" 버튼을 클릭하여 비디오가 아닌 결과를 필터링
        driver.find_element(By.XPATH, "//yt-chip-cloud-chip-renderer[contains(., '동영상')]").click()
    except NoSuchElementException:
        print("Couldn't find the 'Videos' filter button.")
    
    scroll_until_end(driver)
    video_links = extract_video_links(driver)
    
    output_path = r'C:/Users/HAMA/workspace/youtube-py-crawler/data'
    for link in video_links:
        video_code = link.split('/')[-1].split('&')[0]
        download_youtube_video(video_url=link, output_path=output_path, filename=video_code)
    
    driver.quit()

if __name__ == '__main__':
    main('행복하지말아요')
