import os

from pytube import YouTube
from custom_webdriver import CustomWebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils import time_sleep

class YoutubeCrawler:
    # search_base_url = 'https://www.youtube.com/results?search_query={}'
    
    def __init__(
        self, custom_webdriver:CustomWebDriver, keyword:str) -> None:
        self.custom_webdriver = custom_webdriver
        self.keyword = keyword
    
    def run(self):
        self.custom_webdriver.set_web_driver()
        driver = self.custom_webdriver.web_driver

        search_result_url = self.search_base_url.format(self.keyword)
        driver.get(search_result_url)
        
        # "동영상" 섹션 선택
        btn_only_video = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[1]/yt-chip-cloud-renderer/div/div[2]/iron-selector/yt-chip-cloud-chip-renderer[3]/yt-formatted-string')
        btn_only_video.click()
        
        thumbnail_elements = driver.find_elements(By.ID, 'thumbnail')
        for element in thumbnail_elements:
            print(element.get_attribute('href'))
        # self.scroll()
        # self.click_only_video(driver=driver)
        
    def scroll(self):
        scroll_count = 0
        while True:
            try:
                self.custom_webdriver.web_driver.find_element(By.XPATH, '//*[@id="message"]').text
                break
            except NoSuchElementException:
                self.custom_webdriver.web_driver.execute_script("window.scrollBy(0, 1000);")
                scroll_count += 1

    def get_content(self):
        self.custom_webdriver.set_web_driver()
        driver = self.custom_webdriver.web_driver

        
    
    def download(self, video_url, path):
        yt = YouTube(video_url)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not os.path.exists(path):
            os.makedirs(path)
        yt.download(path)
        
        
        
# <a id="thumbnail" class="yt-simple-endpoint inline-block style-scope ytd-thumbnail" aria-hidden="true" tabindex="-1" rel="null" href="/watch?v=aptwVDV16lg&amp;pp=ygUJ7KSE64SY6riw">
#   <yt-image alt="" ftl-eligible="" notify-on-loaded="" notify-on-unloaded="" class="style-scope ytd-thumbnail"><img alt="" style="background-color: transparent;" class="yt-core-image yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded" src="https://i.ytimg.com/vi/aptwVDV16lg/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&amp;rs=AOn4CLDi8aWn6vo3Hdmio75j1UtrjfbTQw"></yt-image>
  
#   <div id="overlays" class="style-scope ytd-thumbnail"><ytd-thumbnail-overlay-time-status-renderer class="style-scope ytd-thumbnail" enable-desktop-round-overlay-thumbnail="" hide-time-status="" overlay-style="DEFAULT"><!--css-build:shady--><!--css-build:shady--><ytd-badge-supported-renderer is-thumbnail-badge="" class="style-scope ytd-thumbnail-overlay-time-status-renderer" system-icons="" enable-refresh-web="" enable-signature-moments-web=""><!--css-build:shady--><!--css-build:shady--><dom-repeat id="repeat" as="badge" class="style-scope ytd-badge-supported-renderer"><template is="dom-repeat"></template></dom-repeat></ytd-badge-supported-renderer><div class="thumbnail-overlay-badge-shape style-scope ytd-thumbnail-overlay-time-status-renderer"><badge-shape class="badge-shape-wiz badge-shape-wiz--thumbnail-default badge-shape-wiz--thumbnail-badge" role="img" aria-label="2분 31초"><div class="badge-shape-wiz__text">2:31</div></badge-shape></div><div id="time-status" class="style-scope ytd-thumbnail-overlay-time-status-renderer" hidden=""><yt-icon size="16" class="style-scope ytd-thumbnail-overlay-time-status-renderer" disable-upgrade="" hidden=""></yt-icon><span id="text" class="style-scope ytd-thumbnail-overlay-time-status-renderer" aria-label="2분 31초">
#     2:31
#   </span></div></ytd-thumbnail-overlay-time-status-renderer><ytd-thumbnail-overlay-now-playing-renderer class="style-scope ytd-thumbnail" now-playing-badge=""><!--css-build:shady--><!--css-build:shady--><span id="overlay-text" class="style-scope ytd-thumbnail-overlay-now-playing-renderer">지금 재생 중</span>
# <ytd-thumbnail-overlay-equalizer class="style-scope ytd-thumbnail-overlay-now-playing-renderer"><!--css-build:shady--><!--css-build:shady--><svg xmlns="http://www.w3.org/2000/svg" id="equalizer" viewBox="0 0 55 95" class="style-scope ytd-thumbnail-overlay-equalizer">
#   <g class="style-scope ytd-thumbnail-overlay-equalizer">
#     <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="0"></rect>
#     <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="20"></rect>
#     <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="40"></rect>
#   </g>
# </svg>
# </ytd-thumbnail-overlay-equalizer>
# </ytd-thumbnail-overlay-now-playing-renderer></div>
#   <div id="mouseover-overlay" class="style-scope ytd-thumbnail"></div>
#   <div id="hover-overlays" class="style-scope ytd-thumbnail"></div>
# </a>