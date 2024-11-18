import time
from tempfile import mkdtemp

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from download_youtube_video import download_youtube_video


def web_driver_options():
    chrome_option_object = webdriver.ChromeOptions()
    chrome_option_object.add_argument('--headless')
    chrome_option_object.add_argument('--no-sandbox')
    chrome_option_object.add_argument("--disable-gpu")
    chrome_option_object.add_argument("--window-size=1280x1696")
    chrome_option_object.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    chrome_option_object.add_argument("single-process")
    chrome_option_object.add_argument("--disable-dev-shm-usage")
    chrome_option_object.add_argument("--disable-dev-tools")
    chrome_option_object.add_argument("--no-zygote")
    chrome_option_object.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_option_object.add_argument(f"--data-path={mkdtemp()}")
    chrome_option_object.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_option_object.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_option_object.add_experimental_option("excludeSwitches", ["enable-automation"])
    return chrome_option_object

def web_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=web_driver_options())
    return driver
    
def main(keyword):
    url = f'https://www.youtube.com/results?search_query={keyword}'
    driver = web_driver()
    driver.get(url)   
    
    watch_btn = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[1]/yt-chip-cloud-renderer/div/div[2]/iron-selector/yt-chip-cloud-chip-renderer[3]/yt-formatted-string')
    watch_btn.click()
    
    scroll_count = 0
    while True:
        if scroll_count > 1000:
            break
        try:
            driver.find_element(By.XPATH, '//*[@id="message"]').text
            break
        except NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 1000);")
            scroll_count += 1

    time.sleep(5)
    for section_idx in range(1, 40+1):
        for content_idx in range(1, 20+1):
            
            try:
                content = driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{section_idx}]/div[3]/ytd-video-renderer[{content_idx}]')
            except NoSuchElementException:
                continue
            
            link = content.find_element(By.ID, 'thumbnail').get_attribute('href')
            watch = "https://www.youtube.com/watch?v=" in link
            shorts = "https://www.youtube.com/shorts/" in link
            if watch:
                video_code = link.replace('https://www.youtube.com/watch?v=', '')
                video_code = video_code.split('&')[0]
            elif shorts:
                video_code = link.replace('https://www.youtube.com/shorts/', '')
            
            download_youtube_video(video_url=link, output_path=r'C:\Users\HAMA\workspace\youtube-py-crawler\data', filename=video_code)
        
if __name__ == '__main__':
    main('30초 줄넘기')